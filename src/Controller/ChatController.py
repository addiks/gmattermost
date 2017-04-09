
class ChatController:
    __gladeBuilder = None  # Gtk.Builder
    __application = None   # Application
    __window = None        # Gtk.Window
    __channelModel = None  # Mattermost.ChannelModel
    __isWindowOpen = False

    def __init__(self, application, channelModel):
        self.__application = application
        self.__channelModel = channelModel

    def show(self):
        self.__reload()

        if not self.__isWindowOpen:
            self.__isWindowOpen = True
            self.__gladeBuilder = self.__application.createGladeBuilder('chat')
            self.__gladeBuilder.connect_signals(self)
            self.__window = self.__gladeBuilder.get_object('windowChat')
            self.__window.show_all()
            self.__reload()

        else:
            self.__window.present()

    def onWindowDestroyed(self, event, userData=None):
        self.__isWindowOpen = False

    def __reload(self):
        pass
