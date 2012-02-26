import compiler
import glob
import os
import pkgutil
import sys

from pysmell.codefinder import CodeFinder

PYSMELL_PREFIX = '__package____module__.'


class PyPlete(object):

    def __init__(self, func_info=None, pythonpath=None, separator='.', *args, **kwargs):
        super(PyPlete, self).__init__(*args, **kwargs)
        if func_info:
            self.func_info = func_info
        if pythonpath:
            self.pythonpath = pythonpath
        else:
            self.pythonpath = sys.path
        self.separator = separator
        self.get_importables_top_level([])

    def func_info(self, name, icon):
        return (name, icon)

    def get_importables_top_level(self, list_autocomplete, use_cache=True):
        # http://code.google.com/p/djangode/source/browse/trunk/djangode/data/codemodel/codemodel.py#57
        if use_cache and getattr(self, 'importables_top_level', None):
            list_autocomplete.extend(self.importables_top_level)
            return bool(len(list_autocomplete))
        self.importables_top_level = []
        self.importables_path = {}
        for directory in self.pythonpath:
            for filename in glob.glob(directory + os.sep + "*"):
                name = None
                if filename.endswith(".py"):
                    name = filename.split(os.sep)[-1][:-3]
                    icon = 'module'
                elif os.path.isdir(filename) and os.path.exists(filename + os.sep + "__init__.py"):
                    name = filename.split(os.sep)[-1]
                    icon = 'package'
                if not name:
                    continue
                importable = self.func_info(name, icon)
                if importable and not importable in self.importables_top_level:
                    self.importables_top_level.append(importable)
                    self.importables_path[name] = [filename]
        list_autocomplete.extend(self.importables_top_level)
        return list_autocomplete and bool(len(list_autocomplete))

    def get_importables_rest_level(self, list_autocomplete, imp_name, subimportables=None, into_module=True):
        imp_path = self.importables_path[imp_name][0]
        subimportables = [subimportable for subimportable in subimportables if subimportable]
        if subimportables:
            subimportables = os.sep.join(subimportables)
            imp_path = "%s%s%s" % (imp_path, os.sep, subimportables)
        for loader, imp_name, is_pkg in pkgutil.walk_packages([imp_path]):
            icon = is_pkg and 'package' or 'module'
            importable = self.func_info(imp_name, icon)
            list_autocomplete.append(importable)
        if into_module:
            into_dir = os.sep.join(imp_path.split(os.sep)[:-1])
            into_module = imp_path.split(os.sep)[-1].replace('.py', '').replace('.pyc', '')
            importer = pkgutil.get_importer(into_dir)
            imp = importer.find_module(into_module)
            if imp:
                self.get_importables_from_text(list_autocomplete, imp.get_source())
        return list_autocomplete and bool(len(list_autocomplete))

    def get_importables_from_text(self, list_autocomplete, text, line=None):
        code = compiler.parse(text)
        code_walk = compiler.walk(code, CodeFinder())
        modules = code_walk.modules
        treatment_dict = {'CONSTANTS': self.treatment_pysmell_const,
                          'FUNCTIONS': self.treatment_pysmell_func,
                          'CLASSES': self.treatment_pysmell_cls}
        for key, func in treatment_dict.items():
            pysmell_items = modules[key]
            if isinstance(pysmell_items, dict):
                pysmell_items = pysmell_items.items()
            for pysmell_item in pysmell_items:
                item = func(pysmell_item)
                if not item in list_autocomplete:
                    list_autocomplete.append(item)

        is_auto = len(list_autocomplete) > 0
        if not is_auto and line:
            line = "%s%s" % (PYSMELL_PREFIX, line.strip())
            for pointer in modules['POINTERS'].keys():
                if pointer.startswith(line):
                    is_auto = is_auto or self.get_importables_from_line(list_autocomplete,
                                            text, pointer.replace(PYSMELL_PREFIX, ''),
                                            text_info=False)
        return is_auto

    def get_importables_from_line(self, list_autocomplete, text, code_line, text_info=True):
        code = compiler.parse(text)
        code_walk = compiler.walk(code, CodeFinder())
        code_line_split = code_line.split(self.separator)
        prefix = code_line_split[0]
        prfx_code_line = '%s%s' % (PYSMELL_PREFIX, prefix)
        if prfx_code_line in code_walk.modules['CONSTANTS']:
            return False
        elif code_walk.modules['CLASSES'].get(prfx_code_line, None) and not code_line_split[1:]:
            class_smell = code_walk.modules['CLASSES'].get(prfx_code_line)
            self.treatment_pysmell_into_cls(class_smell, list_autocomplete)
            return True
        elif prfx_code_line in [name for name, args, desc in code_walk.modules['FUNCTIONS']]:
            index_func = [f[0] for f in code_walk.modules['FUNCTIONS']].index(prfx_code_line)
            func_smell = code_walk.modules['FUNCTIONS'][index_func]
            list_autocomplete.append(self.treatment_pysmell_into_func(func_smell))
            return True
        elif code_walk.modules['POINTERS'].get(prfx_code_line, None):
            module_path = code_walk.modules['POINTERS'].get(prfx_code_line, None)
            module = module_path.split(self.separator)[0]
            submodules = module_path.split(self.separator)[1:]
            submodules.extend(code_line_split[1:])
            imp_loader, submodules_undone = self.get_imp_loader_from_path(module, submodules)
            if not submodules_undone:
                self.get_importables_rest_level(list_autocomplete, module, submodules, True)
            submodules_undone.reverse()
            line = self.separator.join(submodules_undone)
            text = imp_loader.get_source()
            if line:
                return self.get_importables_from_line(list_autocomplete, text, line)
            if text_info:
                return self.get_importables_from_text(list_autocomplete, text, list_autocomplete)
        return False

    def get_imp_loader_from_path(self, imp_name, subimportables, subimportables_undone=None):
        imp_path = self.importables_path[imp_name][0]
        subimportables_undone = subimportables_undone or []
        subimportables_str = os.sep.join(subimportables)
        if subimportables_str:
            imp_path = "%s%s%s" % (imp_path, os.sep, subimportables_str)
        into_dir = os.sep.join(imp_path.split(os.sep)[:-1])
        into_module = imp_path.split(os.sep)[-1].replace('.py', '').replace('.pyc', '')
        importer = pkgutil.get_importer(into_dir)
        importable = importer.find_module(into_module)
        if importable:
            return (importable, subimportables_undone)
        elif subimportables:
            subimportables_undone.append(subimportables[-1])
            return self.get_module_from_path(imp_name, subimportables[:-1], subimportables_undone)
        return (None, subimportables_undone)

    def treatment_pysmell_const(self, constant):
        constant = constant.replace(PYSMELL_PREFIX, '')
        return self.func_info(constant, 'constant')

    def treatment_pysmell_func(self, func):
        func_name, args, description = func
        func_name = func_name.replace(PYSMELL_PREFIX, '')
        args = ', '.join(args)
        args = ' (%s)' % args
        return self.func_info(func_name,
                              'function', args, description)

    def treatment_pysmell_into_func(self, func):
        return self.treatment_pysmell_func(func)

    def treatment_pysmell_cls(self, cls):
        cls_name, info = cls
        cls_name = cls_name.replace(PYSMELL_PREFIX, '')
        args_constructor = info.get('constructor', None)
        args_constructor = ', '.join(args_constructor)
        args_constructor = ' (%s)' % args_constructor
        description = info.get('docstring', None)
        return self.func_info(cls_name,
                             'class', args_constructor,
                             description)

    def treatment_pysmell_into_cls(self, cls, list_autocomplete):
        for m in cls['methods']:
            item = self.treatment_pysmell_func(m)
            if not item in list_autocomplete:
                list_autocomplete.append(item)
        for m in cls['constructor']:
            item = self.treatment_pysmell_func(m)
            if not item in list_autocomplete:
                list_autocomplete.append(item)
        for m in cls['properties']:
            item = self.treatment_pysmell_const(m)
            if not item in list_autocomplete:
                list_autocomplete.append(item)
