
from .ChatController import ChatController

class TeamController:
    __gladeBuilder = None     # Gtk.Builder
    __application = None      # Application
    __window = None           # Gtk.Window
    __serverModel = None      # Mattermost.ServerModel
    __loggedInModel = None    # Mattermost.ServerLoggedInModel
    __teamModel = None        # Mattermost.TeamModel
    __channelControllers = {} # ChatController[]

    def __init__(self, application, url, username, password, teamName):
        self.__application = application

        self.__gladeBuilder = application.createGladeBuilder('team')
        self.__gladeBuilder.connect_signals(self)

        self.__window = self.__gladeBuilder.get_object('windowTeam')

        self.__serverModel = application.getServerModel(url)

        self.__loggedInModel = self.__serverModel.login(username, password)

        self.__teamModel = self.__loggedInModel.getTeam(teamName)

    def show(self):
        self.__reload()
        self.__window.show_all()

    def getChatController(self, channelId):
        if channelId not in self.__chatControllers:
            # Mattermost.ChannelModel
            channelModel = self.__teamModel.getChannel(channelId)

            chatController = ChatController(self.__application, channelModel)

            self.__chatControllers[channelId] = chatController
        return self.__chatControllers[channelId]

    def onTeamChannelRowActivated(self, treeView, treePath, column, data=None):
        # Gtk.TreeView
        # Gtk.TreePath
        # Gtk.TreeViewColumn

        # Gtk.Builder
        gladeBuilder = self.__gladeBuilder

        # Gtk.ListStore
        liststoreTeamChannels = gladeBuilder.get_object('liststoreTeamChannels')

        # Gtk.TreeIter
        treeIter = liststoreTeamChannels.get_iter(treePath)

        channelId = liststoreTeamChannels.get_value(treeIter, 1)

        # ChatController
        chatController = self.getChatController(channelId)
        chatController.show()

    def __reload(self):
        # MattermostTeamModel
        teamModel = self.__teamModel

        # Gtk.Builder
        gladeBuilder = self.__gladeBuilder

        # Gtk.ListStore
        liststoreTeamChannels = gladeBuilder.get_object('liststoreTeamChannels')

        # Gtk.ListStore
        liststoreTeamPrivateGroups = gladeBuilder.get_object('liststoreTeamPrivateGroups')

        # Gtk.ListStore
        liststoreTeamDirectMessages = gladeBuilder.get_object('liststoreTeamDirectMessages')

        for channel in teamModel.getChannels():
            # Mattermost.ChannelModel

            if channel.isOpen():
                # Gtk.TreeIter
                treeIter = liststoreTeamChannels.append()

                liststoreTeamChannels.set_value(treeIter, 0, channel.getDisplayName())
#                liststoreTeamChannels.set_value(treeIter, 1, int(channel.getId()))

            if channel.isDirectMessage():
                # Gtk.TreeIter
                treeIter = liststoreTeamDirectMessages.append()

                # UserModel
                remoteUser = channel.getDirectMessageRemoteUser()

                displayName = "[unknown]"
                if remoteUser != None:
                    displayName = remoteUser.getUseName()

                liststoreTeamDirectMessages.set_value(treeIter, 0, displayName)

            if channel.isPrivateGroup():
                # Gtk.TreeIter
                treeIter = liststoreTeamPrivateGroups.append()

                liststoreTeamPrivateGroups.set_value(treeIter, 0, channel.getDisplayName())
