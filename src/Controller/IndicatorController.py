
from gi.repository import AppIndicator3 as appindicator

class IndicatorController:
    __application = None # Application
    __indicator = None   # appindicator.Indicator

    def __init__(self, application):

        # Gtk.Builder
        self.__gladeBuilder = application.createGladeBuilder('indicator')
        self.__gladeBuilder.connect_signals(self)

        menuIndicator = self.__gladeBuilder.get_object('menuIndicator')

        indicator = appindicator.Indicator.new (
            "example-simple-client",
            "indicator-messages",
            appindicator.IndicatorCategory.APPLICATION_STATUS
        )
        indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        indicator.set_attention_icon("indicator-messages-new")
        indicator.set_menu(menuIndicator)

        self.__indicator = indicator
        self.__application = application

    def onQuitPressed(self, menuItem):
        self.__application.shutdown()

    def onShowListOfTeamsPressed(self, menuItem):
        self.__application.showTeamsListWindow(True, False)
