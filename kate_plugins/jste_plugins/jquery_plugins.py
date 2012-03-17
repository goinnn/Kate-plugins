import kate

from kate_core_plugins import insertText, TEXT_TO_CHANGE
from kate_settings_plugins import KATE_ACTIONS

TEXT_JQUERY = """<script type="text/javascript">
    (function($){
        $(document).ready(function () {
            $("%s").click(function(){
                // Write here
            });
        });
      })(jQuery);
</script>
"""


@kate.action(**KATE_ACTIONS['insertReady'])
def insertReady():
    insertText(TEXT_JQUERY % TEXT_TO_CHANGE, start_in_current_column=True)
