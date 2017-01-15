
import httplib2
import json

# https://api.mattermost.com/

class MattermostServerModel:
    __http = None
    __url = None
    __token = None
    __teamName = None
    __isReachable = None

    def __init__(self, url):
        while url[-1] == "/" and len(url) > 0:
            url = url[0:-1]
        self.__url = url
        self.__http = httplib2.Http(".cache")

    def ping(self):
        url = self.__url + "/api/v3"

        isReachable = False

        try:
            responseHeaders, contentJson = self.__http.request(url, "GET")
            if type(contentJson) == bytes:
                contentJson = contentJson.decode()
            try:
                content = json.loads(contentJson)
                if type(content) == dict and 'id' in content and content['id'] == 'api.context.404.app_error':
                    isReachable = True
            except:
                pass
        except:
            pass

        self.__isReachable = isReachable

    def isReachable(self):
        if self.__isReachable == None:
            self.ping()
        return self.__isReachable

    def login(self, username, password):

        if not self.isReachable():
            raise Exception("Mattermost-Server %s is not reachable!" % self.__url)

        url = self.__url + "/api/v3/users/login"

        responseHeaders, contentJson = self.__http.request(url, "POST", body=json.dumps({
            'login_id': username,
            'password': password
        }))

        if type(contentJson) == bytes:
            contentJson = contentJson.decode()

        content = json.loads(contentJson)

        if "token" in responseHeaders:
            self.__token = responseHeaders['token']

        elif "message" in content:
            raise Exception("Server response: %s" % content['message'])

        else:
            raise Exception("Cannot login on this server!")

    def createUser(self):
        headers, result = self.__callServer("POST", "/users/create")

    def getUser(self):
        headers, result = self.__callServer("GET", "/users/me")

    def logout(self):
        headers, result = self.__callServer("POST", "/users/logout")

    def getUsers(self):
        headers, result = self.__callServer("GET", "/users/{offset}/{limit}")

    def getUsersByTeam(self):
        headers, result = self.__callServer("GET", "/teams/{team_id}/users/{offset}/{limit}")

    def searchUsers(self):
        headers, result = self.__callServer("POST", "/users/search")

    def getUsersByIds(self):
        headers, result = self.__callServer("POST", "/users/ids")

    def getUsersInChannel(self):
        headers, result = self.__callServer("POST", "/teams/{team_id}/channels/{channel_id}/users/{offset}/{limit}")

    def getUsersNotInChannel(self):
        headers, result = self.__callServer("POST", "/teams/{team_id}/channels/{channel_id}/users/not_in_channel/{offset}/{limit}")

    def updateUser(self):
        headers, result = self.__callServer("POST", "/users/update")

    def updateUserRoles(self):
        headers, result = self.__callServer("POST", "/users/update_roles")

    def updateUserIsActive(self):
        headers, result = self.__callServer("POST", "/users/update_active")

    def updateUserNotificationProperties(self):
        headers, result = self.__callServer("POST", "/users/update_notify")

    def updateUserPassword(self):
        headers, result = self.__callServer("POST", "/users/newpassword")

    def sendPasswordResetMail(self):
        headers, result = self.__callServer("POST", "/users/send_password_reset")

    def autocompleteUsersInTeam(self):
        headers, result = self.__callServer("GET", "/teams/{team_id}/users/autocomplete")

    def autocompleteUsersInChannel(self):
        headers, result = self.__callServer("GET", "/teams/{team_id}/channels/{channel_id}/users/autocomplete")

    def createTeam(self):
        headers, result = self.__callServer("POST", "/teams/create")

    def listTeams(self): # TODO: resolve this alias
        return self.getAllTeams()

    def getAllTeams(self):
        headers, teams = self.__callServer("GET", "/teams/all")
        return teams

    def getTeamMembers(self):
        headers, result = self.__callServer("GET", "/teams/{team_id}/members/{offset}/{limit}")

    def getTeamMember(self):
        headers, result = self.__callServer("GET", "/teams/{team_id}/members/{user_id}")

    def getTeamMembersByIds(self):
        headers, result = self.__callServer("POST", "/teams/{team_id}/members/ids")

    def getTeam(self):
        headers, result = self.__callServer("GET", "/teams/{team_id}/me")

    def updateTeam(self):
        headers, result = self.__callServer("POST", "/teams/{team_id}/update")

    def getTeamStatistics(self):
        headers, result = self.__callServer("GET", "/teams/{team_id}/stats")

    def addUserToTeam(self):
        headers, result = self.__callServer("POST", "/teams/{team_id}/add_user_to_team")

    def removeUserFromTeam(self):
        headers, result = self.__callServer("POST", "/teams/{team_id}/remove_user_from_team")

    def createChannel(self):
        headers, result = self.__callServer("POST", "/teams/{team_id}/channels/create")

    def updateChannel(self):
        headers, result = self.__callServer("POST", "/teams/{team_id}/channels/update")

    def deleteChannel(self):
        headers, result = self.__callServer("POST", "/teams/{team_id}/channels/{channel_id}/delete")

    def getChannels(self):
        headers, result = self.__callServer("GET", "/teams/{team_id}/channels")

    def getMoreChannels(self):
        headers, result = self.__callServer("GET", "/teams/{team_id}/channels/more")

    def getChannelMembers(self):
        headers, result = self.__callServer("GET", "/teams/{team_id}/channels/members")

    def getChannel(self):
        headers, result = self.__callServer("GET", "/teams/{team_id}/channels/{channel_id}")

    def getChannelStatistics(self):
        headers, result = self.__callServer("GET", "/teams/{team_id}/channels/{channel_id}/stats")

    def addUserToChannel(self):
        headers, result = self.__callServer("POST", "/teams/{team_id}/channels/{channel_id}/add")

    def getChannelMember(self):
        headers, result = self.__callServer("GET", "/teams/{team_id}/channels/{channel_id}/members/{user_id}")

    def serachPosts(self):
        headers, result = self.__callServer("POST", "/teams/{team_id}/posts/search")

    def serachFlaggedPosts(self):
        headers, result = self.__callServer("GET", "/teams/{team_id}/flagged/{offset}/{limit}")

    def createPost(self):
        headers, result = self.__callServer("POST", "/teams/{team_id}/channels/{channel_id}/posts/create")

    def updatePost(self):
        headers, result = self.__callServer("POST", "/teams/{team_id}/channels/{channel_id}/posts/update")

    def getPostsByChannel(self):
        headers, result = self.__callServer("GET", "/teams/{team_id}/channels/{channel_id}/posts/page/{offset}/{limit}")

    def getPostsByChannelSinceTime(self):
        headers, result = self.__callServer("GET", "/teams/{team_id}/channels/{channel_id}/posts/since/{time}")

    def getPost(self):
        headers, result = self.__callServer("GET", "/teams/{team_id}/channels/{channel_id}/posts/{post_id}/get")

    def deletePost(self):
        headers, result = self.__callServer("GET", "/teams/{team_id}/channels/{channel_id}/posts/{post_id}/delete")

    def getPostsBeforePost(self):
        headers, result = self.__callServer("GET", "/teams/{team_id}/channels/{channel_id}/posts/{post_id}/before/{offset}/{limit}")

    def getPostsAfterPost(self):
        headers, result = self.__callServer("GET", "/teams/{team_id}/channels/{channel_id}/posts/{post_id}/after/{offset}/{limit}")

    def uploadFile(self):
        headers, result = self.__callServer("POST", "/teams/{team_id}/files/upload")

    def getFile(self):
        headers, result = self.__callServer("GET", "/files/{file_id}/get")

    def getFileThumbnail(self):
        headers, result = self.__callServer("GET", "/files/{file_id}/get_thumbnail")

    def getFilePreview(self):
        headers, result = self.__callServer("GET", "/files/{file_id}/get_preview")

    def getFileInfo(self):
        headers, result = self.__callServer("GET", "/files/{file_id}/get_info")

    def getFilePublicLink(self):
        headers, result = self.__callServer("GET", "/files/{file_id}/get_public_link")

    def savePreferences(self):
        headers, result = self.__callServer("POST", "/preferences/save")

    def deletePreferences(self):
        headers, result = self.__callServer("POST", "/preferences/delete")

    def getPreferences(self):
        headers, result = self.__callServer("GET", "/preferences/{category}")

    def getPreference(self):
        headers, result = self.__callServer("GET", "/preferences/{category}/{name}")

    def getIncomingWebhooks(self):
        headers, result = self.__callServer("GET", "/teams/{team_id}/hooks/incoming/list")

    def createIncomingWebhook(self):
        headers, result = self.__callServer("POST", "/teams/{team_id}/hooks/incoming/create")

    def deleteIncomingWebhook(self):
        headers, result = self.__callServer("GET", "/teams/{team_id}/hooks/incoming/delete")

    def teamExists(self, teamName):
        foundTeam = False
        for team in self.listTeams():
            if team['display_name'] == teamName:
                foundTeam = True
                break
        return foundTeam

    def selectTeam(self, teamName):
        if not self.teamExists(teamName):
            raise Exception("Team %s does not exist or is not accessable for this user!" % teamName)
        self.__teamName = teamName

    def __callServer(self, method, route, data=None):
        if not self.isReachable():
            raise Exception("Mattermost-Server %s is not reachable!" % self.__url)

        if self.__token == None:
            raise Exception("Mattermost-Server %s is not logged in!" % self.__url)

        url = self.__url + "/api/v3" + route

        headers = {
            'Authorization': "Bearer " + self.__token
        }

        dataJson = None
        if data != None:
            dataJson = json.dumps(data)

        responseHeaders, contentJson = self.__http.request(
            url,
            method,
            body=dataJson,
            headers=headers
        )

        if type(contentJson) == bytes:
            contentJson = contentJson.decode()

        content = json.loads(contentJson)

        return responseHeaders, content
