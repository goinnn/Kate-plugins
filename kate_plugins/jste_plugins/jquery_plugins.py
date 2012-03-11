import kate

from kate_core_plugins import insertText, setSelectionFromCurrentPosition
from kate_settings_plugins import KATE_ACTIONS

TEXT_JQUERY = """<script type="text/javascript">
    (function($){
        $(document).ready(function () {
            $("XXX").click(function(){
                // Write here
            });
        });
      })(jQuery);
</script>
"""


@kate.action(**KATE_ACTIONS['insertReady'])
def insertReady():
    view = kate.activeView()
    pos = view.cursorPosition()
    insertText(TEXT_JQUERY, start_in_current_column=True)
    setSelectionFromCurrentPosition(pos, (3, 15), (3, 18))
