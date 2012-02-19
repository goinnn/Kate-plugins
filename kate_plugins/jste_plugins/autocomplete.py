import kate

from PyQt4 import QtCore

from autopate import AbstractJSONFileCodeCompletionModel


class StaticJSCodeCompletionModel(AbstractJSONFileCodeCompletionModel):

    MIMETYPES = ['js', 'html', 'htm']
    FILE_PATH = 'jste_plugins/autocomplete_js.json'
    OPERATORS = ["=", " ", "[", "]", "(", ")", "{", "}", ":", ">", "<",
                 "+", "-", "*", "/", "%", " && ", " || ", ","]

    # File generated with this script:
    #function getIcon(child, childKey) {
        #if (!child) {
            #return "constant";
        #}
        #try {
            #var toString = child['toString'];
            #var repr = toString();
        #} catch(e) {
            #return "constant";
        #}
        #if (repr == "[object "+ childKey +"]" ) {
            #return "class";
        #} else if (repr.indexOf("[object ")) {
            #return "module";
        #}
        #return "function";
    #}

    #function getJSAutocomplete(obj, levelmax, level, dict) {
        #if (!dict) {
            #dict = {}
        #}
        #if (level == undefined) {
            #level = 0;
        #} else {
            #level++;
        #}
        #for (var childKey in obj){
            #children = {};
            #var child = null;
            #var childKeyInt = parseInt(childKey);
            #if (childKey != "window" && !childKeyInt && childKeyInt!=0) {
                #try {
                    #child = obj[childKey];
                    #if (level < levelmax) {
                        #children = getJSAutocomplete(child, levelmax, level, children);
                    #}
                #} catch(e) {
                #}
                #dict[childKey] = {"children": children};
                #if (child) {
                    #dict[childKey]["icon"] = getIcon(child, childKey);
                #}
            #}
        #}
        #return dict
    #}
    #result = JSON.stringify(getJSAutocomplete(window, 2))

    #After in a python shell:
    #import simplejson
    #import pprint
    #json_text = open("./autocomplete_js.json").read()
    #pp = pprint.PrettyPrinter(indent=1)
    #file = open("./autocomplete_js.json", "w")
    #target = pp.pformat(simplejson.loads(json_text))
    #file.write(target.replace("'", '"'))
    #file.close()


def createSignalAutocompleteDocument(view, *args, **kwargs):
    cci = view.codeCompletionInterface()
    cci.registerCompletionModel(jscodecompletationmodel)

windowInterface = kate.application.activeMainWindow()
jscodecompletationmodel = StaticJSCodeCompletionModel(windowInterface)
windowInterface.connect(windowInterface,
                QtCore.SIGNAL('viewCreated(KTextEditor::View*)'),
                createSignalAutocompleteDocument)
