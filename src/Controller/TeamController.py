
import os

from gi.repository import Gtk, GdkPixbuf, Gio
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
        if channelId not in self.__channelControllers:
            # Mattermost.ChannelModel
            channelModel = self.__teamModel.getChannel(channelId)

            chatController = ChatController(self.__application, channelModel)

            self.__channelControllers[channelId] = chatController
        return self.__channelControllers[channelId]

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

        # Gtk.Image
        imageTeamAvatar = gladeBuilder.get_object('imageTeamAvatar')

        # UserModel
        selfUser = self.__loggedInModel.getSelfUser()

        cacheId = "avatar." + selfUser.getId() + ".png"
        avatarImagePath = self.__application.getCacheFilePath(cacheId)

        if not os.path.exists(avatarImagePath):
            avatarImageData = selfUser.getImage()
            self.__application.putCache(cacheId, avatarImageData)

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            avatarImagePath,
            width=48,
            height=48,
            preserve_aspect_ratio=False
        )

        imageTeamAvatar.set_from_pixbuf(pixbuf)

#        avatarUrl = teamModel.getAvatarIconUrl()
#        imageTeamAvatar.set_from_file(avatarUrl)

        variables = {
            'USERNAME': selfUser.getUseName(),
            'TEAMNAME': teamModel.getName()
        }

        for labelId in ["labelTeamNamesUsername", "labelTeamNamesTeam"]:
            # Gtk.Label
            label = gladeBuilder.get_object(labelId)

            templateText = label.get_text()
            for variableKey in variables:
                templateText = templateText.replace("%"+variableKey+"%", variables[variableKey])
            label.set_text(templateText)

        directMessageUserIdToTreeIterMap = {}

        for channel in teamModel.getChannels():
            # Mattermost.ChannelModel

            if channel.isOpen():
                # Gtk.TreeIter
                treeIter = liststoreTeamChannels.append()

                liststoreTeamChannels.set_value(treeIter, 0, channel.getDisplayName())
                liststoreTeamChannels.set_value(treeIter, 1, channel.getId())

            if channel.isDirectMessage():
                # Gtk.TreeIter
                treeIter = liststoreTeamDirectMessages.append()

                remoteUserId = channel.getDirectMessageRemoteUserId()

                directMessageUserIdToTreeIterMap[remoteUserId] = treeIter

                liststoreTeamDirectMessages.set_value(treeIter, 1, remoteUserId)

            if channel.isPrivateGroup():
                # Gtk.TreeIter
                treeIter = liststoreTeamPrivateGroups.append()

                liststoreTeamPrivateGroups.set_value(treeIter, 0, channel.getDisplayName())

        # Load all direct-message remote users at once
        remoteUsers = self.__loggedInModel.getUsersByIds(list(directMessageUserIdToTreeIterMap))

        for remoteUser in remoteUsers:
            # UserModel

            treeIter = directMessageUserIdToTreeIterMap[remoteUser.getId()]
            liststoreTeamDirectMessages.set_value(treeIter, 0, remoteUser.getUseName())

#
