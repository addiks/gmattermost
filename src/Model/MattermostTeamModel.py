
from .MattermostChannelModel import MattermostChannelModel

class MattermostTeamModel:
    __serverModel = None # MattermostServerLoggedInModel
    __teamId = None
    __createdAt = None
    __updatedAt = None
    __deletedAt = None
    __displayName = None
    __name = None
    __email = None
    __teamType = None       # 'D' = ?; 'O' = ?;
    __allowedDomains = None
    __inviteId = None
    __allowOpenInvite = None

    @staticmethod
    def fromJsonTeamObject(serverModel, data):
        return MattermostTeamModel(
            serverModel,
            data['id'],
            data['create_at'],
            data['update_at'],
            data['delete_at'],
            data['display_name'],
            data['name'],
            data['email'],
            data['type'],
            data['allowed_domains'],
            data['invite_id'],
            data['allow_open_invite']
        )

    def __init__(
        self,
        serverModel,
        teamId,
        createdAt,
        updatedAt,
        deletedAt,
        displayName,
        name,
        email,
        teamType,
        allowedDomains,
        inviteId,
        allowOpenInvite
    ):
        self.__serverModel = serverModel
        self.__teamId = teamId
        self.__createdAt = createdAt
        self.__updatedAt = updatedAt
        self.__deletedAt = deletedAt
        self.__displayName = displayName
        self.__name = name
        self.__email = email
        self.__teamType = teamType
        self.__allowedDomains = allowedDomains
        self.__inviteId = inviteId
        self.__allowOpenInvite = allowOpenInvite

    def getId(self):
        return self.__teamId

    def getName(self):
        return self.__name

    def autocompleteUsersInTeam(self):
        raise Exception("*UNIMPLEMENTED*")
        headers, result = self.callServer("GET", "/users/autocomplete")

    def autocompleteUsersInChannel(self, channelId):
        raise Exception("*UNIMPLEMENTED*")
        headers, result = self.callServer("GET", "/channels/%s/users/autocomplete" % channelId)

    def getTeamMembers(self, offset=0, limit=30):
        raise Exception("*UNIMPLEMENTED*")
        headers, result = self.callServer("GET", "/members/%d/%d" % (offset, limit))

    def getTeamMember(self, userId):
        raise Exception("*UNIMPLEMENTED*")
        headers, result = self.callServer("GET", "/members/%s" % userId)

    def getUsersByTeam(self, offset=0, limit=30):
        raise Exception("*UNIMPLEMENTED*")
        headers, result = self.callServer("GET", "/users/%d/%d" % (offset, limit))

    def getTeamMembersByIds(self):
        raise Exception("*UNIMPLEMENTED*")
        headers, result = self.callServer("POST", "/members/ids")

#   Not needed (?)
#    def getTeam(self):
#        raise Exception("*UNIMPLEMENTED*")
#        headers, result = self.callServer("GET", "/me")

    def updateTeam(self):
        raise Exception("*UNIMPLEMENTED*")
        headers, result = self.callServer("POST", "/update")

    def getTeamStatistics(self):
        raise Exception("*UNIMPLEMENTED*")
        headers, result = self.callServer("GET", "/stats")

    def addUserToTeam(self):
        raise Exception("*UNIMPLEMENTED*")
        headers, result = self.callServer("POST", "/add_user_to_team")

    def removeUserFromTeam(self):
        raise Exception("*UNIMPLEMENTED*")
        headers, result = self.callServer("POST", "/remove_user_from_team")

    def createChannel(self):
        raise Exception("*UNIMPLEMENTED*")
        headers, result = self.callServer("POST", "/channels/create")

    def updateChannel(self):
        raise Exception("*UNIMPLEMENTED*")
        headers, result = self.callServer("POST", "/channels/update")

    def deleteChannel(self, channelId):
        raise Exception("*UNIMPLEMENTED*")
        headers, result = self.callServer("POST", "/channels/%s/delete" % channelId)

    def getChannels(self):
        headers, result = self.callServer("GET", "/channels/")
        print(result)
        channelModels = []

        for channelData in result:
            channelModels.append(MattermostChannelModel.fromJsonTeamObject(self, channelData))

        return channelModels

    def getMoreChannels(self):
        raise Exception("*UNIMPLEMENTED*")
        headers, result = self.callServer("GET", "/channels/more")

    def getChannelMembers(self):
        raise Exception("*UNIMPLEMENTED*")
        headers, result = self.callServer("GET", "/channels/members")

    def getChannel(self, channelId): # return MattermostChannelModel
        raise Exception("*UNIMPLEMENTED*")
        headers, result = self.callServer("GET", "/channels/%s" % channelId)

    def searchPosts(self):
        raise Exception("*UNIMPLEMENTED*")
        headers, result = self.callServer("POST", "/posts/search")

    def searchFlaggedPosts(self, offset=0, limit=30):
        raise Exception("*UNIMPLEMENTED*")
        headers, result = self.callServer("GET", "/flagged/%d/%d" % (offset, limit))

    def uploadFile(self):
        raise Exception("*UNIMPLEMENTED*")
        headers, result = self.callServer("POST", "/files/upload")

    def getIncomingWebhooks(self):
        raise Exception("*UNIMPLEMENTED*")
        headers, result = self.callServer("GET", "/hooks/incoming/list")

    def createIncomingWebhook(self):
        raise Exception("*UNIMPLEMENTED*")
        headers, result = self.callServer("POST", "/hooks/incoming/create")

    def deleteIncomingWebhook(self):
        raise Exception("*UNIMPLEMENTED*")
        headers, result = self.callServer("GET", "/hooks/incoming/delete")

    def callServer(self, method, route, data=None):
        return self.__serverModel.callServer(method, "/teams/%s%s" % (self.__teamId, route), data)
