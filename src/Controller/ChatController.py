
class ChatController:
    __gladeBuilder = None # Gtk.Builder
    __application = None  # Application
    __window = None       # Gtk.Window
    __channelModel = None # Mattermost.ChannelModel

    def __init__(self, application, channelModel):
        self.__application = application

        self.__gladeBuilder = application.createGladeBuilder('chat')
        self.__gladeBuilder.connect_signals(self)

        self.__window = self.__gladeBuilder.get_object('windowChat')

        self.__channelModel = channelModel

    def show(self):
        self.__reload()
        self.__window.show_all()

    def __reload(self):
        pass
