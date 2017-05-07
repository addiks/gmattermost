
class ChatController:
    __gladeBuilder = None        # Gtk.Builder
    __application = None         # Application
    __window = None              # Gtk.Window
    __windowTitleTemplate = None # string
    __channelModel = None        # Mattermost.ChannelModel
    __isWindowOpen = False       # boolean

    def __init__(self, application, channelModel):
        self.__application = application
        self.__channelModel = channelModel

    def show(self):
        if not self.__isWindowOpen:
            self.__isWindowOpen = True
            self.__gladeBuilder = self.__application.createGladeBuilder('chat')
            self.__gladeBuilder.connect_signals(self)
            self.__window = self.__gladeBuilder.get_object('windowChat')
            self.__windowTitleTemplate = self.__window.get_title()
            self.__window.show_all()
            self.__reload()

        else:
            self.__reload()
            self.__window.present()

    def onWindowDestroyed(self, event, userData=None):
        self.__isWindowOpen = False

    def __reload(self):
        # Gtk.Builder
        gladeBuilder = self.__gladeBuilder

        # Gtk.Window
        window = self.__window

        # ChannelModel
        channelModel = self.__channelModel

        # Gtk.ListStore
        liststoreChatContent = gladeBuilder.get_object('liststoreChatContent')

        # TeamModel
        teamModel = self.__channelModel.getTeamModel()

        # ServerLoggedInModel
        serverModel = teamModel.getServer()

        # UserModel
        selfUser = serverModel.getSelfUser()

        variables = {
            'USERNAME': selfUser.getUseName(),
            'NAME': teamModel.getName()
        }

        windowTitle = self.__windowTitleTemplate
        for variableKey in variables:
            windowTitle = windowTitle.replace("%"+variableKey+"%", variables[variableKey])
        window.set_title(windowTitle)

        posts = channelModel.getLastPosts()
        for postId in posts:
            # PostModel
            post = posts[postId]

            user = post.getUser()

            treeIter = liststoreChatContent.append()

            userId = ""
            userName = ""

            if user != None:
                userId = user.getId()
                userName = user.getUseName()

            liststoreChatContent.set_value(treeIter, 0, userId)
            liststoreChatContent.set_value(treeIter, 1, userName)
            liststoreChatContent.set_value(treeIter, 2, post.getMessage())
