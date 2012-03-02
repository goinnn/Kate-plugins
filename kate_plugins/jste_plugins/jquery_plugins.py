import kate

from kate_settings_plugins import kate_plugins_settings
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


@kate.action(**kate_plugins_settings['insertReady'])
def insertReady():
    insertText(TEXT_JQUERY, start_in_current_column=True)
