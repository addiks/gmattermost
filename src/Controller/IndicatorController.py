
from gi.repository import AppIndicator3 as appindicator

class IndicatorController:
    __application = None # Application
    __indicator = None   # appindicator.Indicator

    def __init__(self, application):

        # Gtk.Builder
        self.__gladeBuilder = application.createGladeBuilder('indicator')
        self.__gladeBuilder.connect_signals(self)

        indicator = appindicator.Indicator.new (
            "example-simple-client",
            "indicator-messages",
            appindicator.IndicatorCategory.APPLICATION_STATUS
        )
        indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        indicator.set_attention_icon("indicator-messages-new")

        self.__gladeBuilder.get_object('menuIndicator')

        self.__indicator = indicator

    def onIndicatorPressed(self):
        self.__application.showTeamsListWindow()
