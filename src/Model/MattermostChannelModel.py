

class MattermostChannelModel:
    __teamModel = None # MattermostTeamModel
    __channelId = None

    def __init__(self, teamModel, teamName):
        self.__teamModel = teamModel

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
