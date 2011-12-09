import kate

from utils import insertText

TEXT_JQUERY = """<script type="text/javascript">
    (function($){
        $(document).ready(function () {
            $("XXX").click(function(){
                // Escribe aqui
            });
        });
      })(jQuery);
</script>
"""


@kate.action('JQuery Ready', shortcut='Ctrl+J', menu='Edit')
def insertReady():
    insertText(TEXT_JQUERY, start_in_current_column=True)
