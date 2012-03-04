import kate

from kate_settings_plugins import KATE_ACTIONS
from utils import insertText

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
    insertText(TEXT_JQUERY, start_in_current_column=True)
