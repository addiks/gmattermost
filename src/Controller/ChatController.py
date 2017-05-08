
import json

class ChatController:
    __gladeBuilder = None        # Gtk.Builder
    __application = None         # Application
    __window = None              # Gtk.Window
    __windowTitleTemplate = None # string
    __channelModel = None        # Mattermost.ChannelModel
    __isWindowOpen = False       # boolean
    __postTreeIterMap = {}       # dict(Gtk.TreeIter)

    def __init__(self, application, channelModel):
        self.__application = application
        self.__channelModel = channelModel

        channelModel.registerTypingListener(self.onTypingEvent)
        channelModel.registerPostedListener(self.onMessagePostedEvent)
        channelModel.registerPostEditedListener(self.onMessageEditedEvent)
        channelModel.registerPostDeletedListener(self.onMessageDeletedEvent)

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

    def onTypingEvent(self, data=None):
        # Gtk.Builder
        gladeBuilder = self.__gladeBuilder

        print("onTypingEvent: " + repr(data))

    def onMessagePostedEvent(self, data=None):
        # Gtk.Builder
        gladeBuilder = self.__gladeBuilder

        # Gtk.Window
        window = self.__window

        # Gtk.ListStore
        liststoreChatContent = gladeBuilder.get_object('liststoreChatContent')

        postJson = data['post']
        postData = json.loads(postJson)

        # TODO: load post-model properly

        # Gtk.TreeIter
        treeIter = liststoreChatContent.append()

        self.__postTreeIterMap[postData['id']] = treeIter

        liststoreChatContent.set_value(treeIter, 0, postData['user_id'])
        liststoreChatContent.set_value(treeIter, 1, data['sender_name'])
        liststoreChatContent.set_value(treeIter, 2, postData['message'])

        window.present()

        print("onMessagePostedEvent: " + repr(data))

    def onMessageEditedEvent(self, data=None):
        # Gtk.Builder
        gladeBuilder = self.__gladeBuilder

        # Gtk.ListStore
        liststoreChatContent = gladeBuilder.get_object('liststoreChatContent')

        postJson = data['post']
        postData = json.loads(postJson)

        # Gtk.TreeIter
        treeIter = self.__postTreeIterMap[postData['id']]

        liststoreChatContent.set_value(treeIter, 2, postData['message'])

        print("onMessageEditedEvent: " + repr(data))

    def onMessageDeletedEvent(self, data=None):
        # Gtk.Builder
        gladeBuilder = self.__gladeBuilder

        # Gtk.ListStore
        liststoreChatContent = gladeBuilder.get_object('liststoreChatContent')

        postJson = data['post']
        postData = json.loads(postJson)

        # Gtk.TreeIter
        treeIter = self.__postTreeIterMap[postData['id']]

        liststoreChatContent.remove(treeIter)

        print("onMessageDeletedEvent: " + repr(data))

    def onSubmitButtonPressed(self, button, data=None):
        self.__doSubmit()

    def onChatInputKeyRelease(self, textInput, event, data=None):
         if event.keyval == 65293: # = enter
            self.__doSubmit()

    def __doSubmit(self):
        # Gtk.Builder
        gladeBuilder = self.__gladeBuilder

        # ChannelModel
        channelModel = self.__channelModel

        # Gtk.EntryBuffer
        entrybufferChatInput = gladeBuilder.get_object('entrybufferChatInput')

        message = entrybufferChatInput.get_text()
        channelModel.createPost(message)
        entrybufferChatInput.set_text("", 0)

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
            'CHANNELNAME': channelModel.getName(),
            'TEAMNAME': teamModel.getName(),
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

            self.__postTreeIterMap[postId] = treeIter

            userId = ""
            userName = ""

            if user != None:
                userId = user.getId()
                userName = user.getUseName()

            liststoreChatContent.set_value(treeIter, 0, userId)
            liststoreChatContent.set_value(treeIter, 1, userName)
            liststoreChatContent.set_value(treeIter, 2, post.getMessage())
