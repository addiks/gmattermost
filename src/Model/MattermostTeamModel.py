

class MattermostTeamModel:
    __serverModel = None # MattermostServerLoggedInModel
    __teamId = None

    def __init__(self, serverModel, teamName):
        self.__serverModel = serverModel

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

    def getTeam(self):
        raise Exception("*UNIMPLEMENTED*")
        headers, result = self.callServer("GET", "/me")

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
        raise Exception("*UNIMPLEMENTED*")
        headers, result = self.callServer("GET", "/channels")

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
