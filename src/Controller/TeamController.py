
import os
import json

from _thread import start_new_thread

from gi.repository import GLib, Gtk, GdkPixbuf, Notify
from .ChatController import ChatController
from Mattermost.ChannelModel import ChannelModel

class TeamController:
    __gladeBuilder = None           # Gtk.Builder
    __application = None            # Application
    __window = None                 # Gtk.Window
    __windowTitleTemplate = None    # string
    __serverModel = None            # Mattermost.ServerModel
    __loggedInModel = None          # Mattermost.ServerLoggedInModel
    __teamModel = None              # Mattermost.TeamModel
    __channelControllers = {}       # dict(Mattermost.ChatController)
    __channelTreeIterMap = {}       # dict(Gtk.TreeIter)
    __privateGroupTreeIterMap = {}  # dict(Gtk.TreeIter)
    __directMessageTreeIterMap = {} # dict(Gtk.TreeIter)

    FONT_WEIGHT_NORMAL=400
    FONT_WEIGHT_BOLD=700

    def __init__(self, application, url, username, password, teamName):
        self.__application = application

        self.__gladeBuilder = application.createGladeBuilder('team')
        self.__gladeBuilder.connect_signals(self)

        self.__window = self.__gladeBuilder.get_object('windowTeam')
        self.__windowTitleTemplate = self.__window.get_title()

        self.__serverModel = application.getServerModel(url)

        self.__loggedInModel = self.__serverModel.login(username, password)

        self.__teamModel = self.__loggedInModel.getTeam(teamName)

        self.__loggedInModel.registerPostedListener(self.onMessagePosted)

        # Mattermost.UserModel
        selfUser = self.__loggedInModel.getSelfUser()

        self.__teamModel.registerChannelCreatedListener(self.onChannelCreated, {
            'user_id': selfUser.getId()
        })

    def show(self):
        self.__reload()
        self.__window.show_all()

    def getChatController(self, channel):
        channelId = channel
        if type(channel) == ChannelModel:
            channelId = channel.getId()
        if channelId not in self.__channelControllers:
            if type(channel) != ChannelModel:
                # Mattermost.ChannelModel
                channel = self.__teamModel.getChannel(channelId)

            # ChatController
            chatController = None

            if channel != None:
                chatController = ChatController(self.__application, channel)

            self.__channelControllers[channelId] = chatController
        return self.__channelControllers[channelId]

    def onChannelCreated(self, data=None):
        channelId = data['channel_id']
        teamId = data['team_id']

        # Mattermost.TeamModel
        teamModel = self.__teamModel

        if teamId == teamModel.getId():
            # Mattermost.ChannelModel
            channelModel = teamModel.getChannel(channelId)

            self.__addChannelToView(channelModel)

    def onMessagePosted(self, data=None):

        # Gtk.Builder
        gladeBuilder = self.__gladeBuilder

        # Gtk.ListStore
        liststoreTeamChannels = gladeBuilder.get_object('liststoreTeamChannels')

        # Gtk.ListStore
        liststoreTeamPrivateGroups = gladeBuilder.get_object('liststoreTeamPrivateGroups')

        # Gtk.ListStore
        liststoreTeamDirectMessages = gladeBuilder.get_object('liststoreTeamDirectMessages')

        postJson = data['post']
        postData = json.loads(postJson)

        channelId = postData['channel_id']

        # Mattermost.ChatController
        chatController = self.getChatController(channelId)

        # Mattermost.ChannelModel
        channel = self.__teamModel.getChannel(channelId)

        # Mattermost.UserModel
        user = self.__loggedInModel.getUserById(postData['user_id'])

        # Mattermost.UserModel
        selfUser = self.__loggedInModel.getSelfUser()

        GLib.idle_add(chatController.show)

        if selfUser.getId() != user.getId():
            # Notify.Notification
            notification = Notify.Notification.new("gMattermost", "%s - %s: %s" % (
                channel.getDisplayName(),
                user.getUseName(),
                postData['message']
            ))
            success = notification.show()

        if postData['channel_id'] in self.__channelTreeIterMap:
            # Gtk.TreeIter
            treeIter = self.__channelTreeIterMap[channelId]

            liststoreTeamChannels.set_value(treeIter, 2, self.FONT_WEIGHT_BOLD)

        if postData['channel_id'] in self.__privateGroupTreeIterMap:
            # Gtk.TreeIter
            treeIter = self.__privateGroupTreeIterMap[channelId]

            liststoreTeamPrivateGroups.set_value(treeIter, 2, self.FONT_WEIGHT_BOLD)

        if postData['channel_id'] in self.__directMessageTreeIterMap:
            # Gtk.TreeIter
            treeIter = self.__directMessageTreeIterMap[channelId]

            liststoreTeamDirectMessages.set_value(treeIter, 2, self.FONT_WEIGHT_BOLD)

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

    def onTeamDirectMessageRowActivated(self, treeView, treePath, column, data=None):
        # Gtk.TreeView
        # Gtk.TreePath
        # Gtk.TreeViewColumn

        # Gtk.Builder
        gladeBuilder = self.__gladeBuilder

        # Gtk.ListStore
        liststoreTeamDirectMessages = gladeBuilder.get_object('liststoreTeamDirectMessages')

        # Gtk.TreeIter
        treeIter = liststoreTeamDirectMessages.get_iter(treePath)

        remoteUserId = liststoreTeamDirectMessages.get_value(treeIter, 1)

        for channelModelCandidate in self.__teamModel.getChannels():
            if channelModelCandidate.isDirectMessage():
                remoteUser = channelModelCandidate.getDirectMessageRemoteUser()
                if remoteUser != None and remoteUser.getId() == remoteUserId:
                    channelModel = channelModelCandidate

        if channelModel != None:
            # ChatController
            chatController = self.getChatController(channelModel)
            chatController.show()

    def onTeamPrivateGroupRowActivated(self, treeView, treePath, column, data=None):
        # Gtk.TreeView
        # Gtk.TreePath
        # Gtk.TreeViewColumn

        # Gtk.Builder
        gladeBuilder = self.__gladeBuilder

        # Gtk.ListStore
        liststoreTeamPrivateGroups = gladeBuilder.get_object('liststoreTeamPrivateGroups')

        # Gtk.TreeIter
        treeIter = liststoreTeamPrivateGroups.get_iter(treePath)

        channelId = liststoreTeamPrivateGroups.get_value(treeIter, 1)

        # ChatController
        chatController = self.getChatController(channelId)
        chatController.show()

    def __reload(self):
        # MattermostTeamModel
        teamModel = self.__teamModel

        # Gtk.Builder
        gladeBuilder = self.__gladeBuilder

        # Gtk.Image
        imageTeamAvatar = gladeBuilder.get_object('imageTeamAvatar')

        # Gtk.Window
        window = self.__window

        # UserModel
        selfUser = self.__loggedInModel.getSelfUser()

        cacheId = "avatar." + selfUser.getId() + ".png"
        avatarImagePath = self.__application.getCacheFilePath(cacheId)

        if not os.path.exists(avatarImagePath):
            avatarImageData = selfUser.getImage()
            self.__application.putCache(cacheId, avatarImageData)

        if os.path.exists(avatarImagePath):
            # GdkPixbuf.Pixbuf
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                avatarImagePath,
                width=48,
                height=48,
                preserve_aspect_ratio=False
            )

            imageTeamAvatar.set_from_pixbuf(pixbuf)

        variables = {
            'USERNAME': selfUser.getUseName(),
            'TEAMNAME': teamModel.getName()
        }

        windowTitle = self.__windowTitleTemplate
        for variableKey in variables:
            windowTitle = windowTitle.replace("%"+variableKey+"%", variables[variableKey])
        window.set_title(windowTitle)

        for labelId in ["labelTeamNamesUsername", "labelTeamNamesTeam"]:
            # Gtk.Label
            label = gladeBuilder.get_object(labelId)

            templateText = label.get_text()
            for variableKey in variables:
                templateText = templateText.replace("%"+variableKey+"%", variables[variableKey])
            label.set_text(templateText)

        self.__addChannelsToView(teamModel.getChannels())

    def __addChannelsToView(self, channels):

        # Gtk.Builder
        gladeBuilder = self.__gladeBuilder

        # Gtk.ListStore
        liststoreTeamDirectMessages = gladeBuilder.get_object('liststoreTeamDirectMessages')

        directMessageUserIdToTreeIterMap = {}

        for channel in channels:
            # Mattermost.ChannelModel

            self.__addChannelToView(channel, directMessageUserIdToTreeIterMap)

        # Load all direct-message remote users at once
        # list(Mattermost.UserModel)
        remoteUsers = self.__loggedInModel.getUsersByIds(list(directMessageUserIdToTreeIterMap))

        for remoteUser in remoteUsers:
            # Mattermost.UserModel

            treeIter = directMessageUserIdToTreeIterMap[remoteUser.getId()]
            liststoreTeamDirectMessages.set_value(treeIter, 0, remoteUser.getUseName())

    def __addChannelToView(self, channel, directMessageUserIdToTreeIterMap=None):
        # Mattermost.ChannelModel

        # Gtk.Builder
        gladeBuilder = self.__gladeBuilder

        # Gtk.ListStore
        liststoreTeamChannels = gladeBuilder.get_object('liststoreTeamChannels')

        # Gtk.ListStore
        liststoreTeamPrivateGroups = gladeBuilder.get_object('liststoreTeamPrivateGroups')

        # Gtk.ListStore
        liststoreTeamDirectMessages = gladeBuilder.get_object('liststoreTeamDirectMessages')

        doSetDirectMessageNames = False
        if directMessageUserIdToTreeIterMap == None:
            directMessageUserIdToTreeIterMap = {}
            doSetDirectMessageNames = True

        # TODO: find out if channel's have unread messages

        if channel.isOpen():
            # Gtk.TreeIter
            treeIter = liststoreTeamChannels.append()

            self.__channelTreeIterMap[channel.getId()] = treeIter

            liststoreTeamChannels.set_value(treeIter, 0, channel.getDisplayName())
            liststoreTeamChannels.set_value(treeIter, 1, channel.getId())
            liststoreTeamChannels.set_value(treeIter, 2, self.FONT_WEIGHT_NORMAL) # hasUnreadMessages

        if channel.isDirectMessage():
            # Gtk.TreeIter
            treeIter = liststoreTeamDirectMessages.append()

            self.__directMessageTreeIterMap[channel.getId()] = treeIter

            remoteUserId = channel.getDirectMessageRemoteUserId()

            directMessageUserIdToTreeIterMap[remoteUserId] = treeIter

            if doSetDirectMessageNames:
                # Mattermost.UserModel
                remoteUser = self.__loggedInModel.getUserById(remoteUserId)

                liststoreTeamDirectMessages.set_value(treeIter, 0, remoteUser.getUseName())

            liststoreTeamDirectMessages.set_value(treeIter, 1, remoteUserId)
            liststoreTeamDirectMessages.set_value(treeIter, 2, self.FONT_WEIGHT_NORMAL) # hasUnreadMessages

        if channel.isPrivateGroup():
            # Gtk.TreeIter
            treeIter = liststoreTeamPrivateGroups.append()

            self.__privateGroupTreeIterMap[channel.getId()] = treeIter

            liststoreTeamPrivateGroups.set_value(treeIter, 0, channel.getDisplayName())
            liststoreTeamPrivateGroups.set_value(treeIter, 1, channel.getId())
            liststoreTeamPrivateGroups.set_value(treeIter, 2, self.FONT_WEIGHT_NORMAL) # hasUnreadMessages
#
