

class ChannelModel:
    __teamModel = None # TeamModel
    __channelId = None
    __createdAt = None
    __updatedAt = None
    __deletedAt = None
    __channelType = None
    __displayName = None
    __name = None
    __headerText = None
    __purpose = None
    __lastPostAt = None
    __totalMessageCount = None
    __extraUpdatedAt = None
    __creatorId = None

    @staticmethod
    def fromJsonChannelObject(teamModel, data):

        if data['team_id'] != teamModel.getId():
            pass # TODO: raise Exception

        return ChannelModel(
            teamModel,
            data['id'],
            data['create_at'],
            data['update_at'],
            data['delete_at'],
            data['type'],
            data['display_name'],
            data['name'],
            data['header'],
            data['purpose'],
            data['last_post_at'],
            data['total_msg_count'],
            data['extra_update_at'],
            data['creator_id']
        )

    def __init__(
        self,
        teamModel,
        channelId,
        createdAt,
        updatedAt,
        deletedAt,
        channelType,
        displayName,
        name,
        headerText,
        purpose,
        lastPostAt,
        totalMessageCount,
        extraUpdatedAt,
        creatorId
    ):
        self.__teamModel = teamModel
        self.__channelId = channelId
        self.__createdAt = createdAt
        self.__updatedAt = updatedAt
        self.__deletedAt = deletedAt
        self.__channelType = channelType
        self.__displayName = displayName
        self.__name = name
        self.__headerText = headerText
        self.__purpose = purpose
        self.__lastPostAt = lastPostAt
        self.__totalMessageCount = totalMessageCount
        self.__extraUpdatedAt = extraUpdatedAt
        self.__creatorId = creatorId

    def getId(self):
        return self.__channelId

    def getName(self):
        return self.__name

    def getDisplayName(self):
        return self.__displayName

    def isOpen(self):
        return self.__channelType == 'O'

    def isInviteOnly(self):
        return self.__channelType == 'I'

    def isDirectMessage(self):
        return self.__channelType == 'D'

    def isPrivateGroup(self):
        return self.__channelType == 'P'

    def getDirectMessageRemoteUserId(self):
        remoteUserId = None

        # TeamModel
        teamModel = self.__teamModel

        userIdA, userIdB = self.__name.split('__')

        # ServerLoggedInModel
        server = teamModel.getServer()

        # UserModel
        myUser = server.getSelfUser()

        myUserId = myUser.getId()

        if userIdA == myUserId:
            remoteUserId = userIdB

        else:
            remoteUserId = userIdA

        return remoteUserId

    def getDirectMessageRemoteUser(self):
        remoteUserId = self.getDirectMessageRemoteUserId()

        # UserModel
        remoteUser = server.getUserById(remoteUserId)

        return remoteUser

    def createPost(self):
        raise Exception("*UNIMPLEMENTED*")
        headers, result = self.callServer("POST", "/posts/create")

    def updatePost(self):
        raise Exception("*UNIMPLEMENTED*")
        headers, result = self.callServer("POST", "/posts/update")

    def getPostsByChannel(self, offset=0, limit=30):
        raise Exception("*UNIMPLEMENTED*")
        headers, result = self.callServer("GET", "/posts/page/%d/%d" % (offset, limit))

    def getPostsByChannelSinceTime(self, time):
        raise Exception("*UNIMPLEMENTED*")
        headers, result = self.callServer("GET", "/posts/since/%s" % time)

    def getPost(self, postId):
        raise Exception("*UNIMPLEMENTED*")
        headers, result = self.callServer("GET", "/posts/%s/get" % postId)

    def deletePost(self, postId):
        raise Exception("*UNIMPLEMENTED*")
        headers, result = self.callServer("GET", "/posts/%s/delete" % postId)

    def getPostsBeforePost(self, postId, offset=0, limit=30):
        raise Exception("*UNIMPLEMENTED*")
        headers, result = self.callServer("GET", "/posts/%s/before/%d/%d" % (postId, offset, limit))

    def getPostsAfterPost(self, postId, offset=0, limit=30):
        raise Exception("*UNIMPLEMENTED*")
        headers, result = self.callServer("GET", "/posts/%s/after/%d/%d" % (postId, offset, limit))

    def getChannelStatistics(self):
        raise Exception("*UNIMPLEMENTED*")
        headers, result = self.callServer("GET", "/stats")

    def addUserToChannel(self):
        raise Exception("*UNIMPLEMENTED*")
        headers, result = self.callServer("POST", "/add")

    def getChannelMember(self, userId):
        raise Exception("*UNIMPLEMENTED*")
        headers, result = self.callServer("GET", "/members/%s" % userId)

    def getUsersInChannel(self, offset=0, limit=30):
        raise Exception("*UNIMPLEMENTED*")
        headers, result = self.callServer("POST", "/users/%d/%d" % (offset, limit))

    def getUsersNotInChannel(self, offset=0, limit=30):
        raise Exception("*UNIMPLEMENTED*")
        headers, result = self.callServer("POST", "/users/not_in_channel/%d/%d" % (offset, limit))

    def callServer(self, method, route, data=None):
        return self.__teamModel.callServer(method, "/channels/%s%s" % (self.__channelId, route), data)
