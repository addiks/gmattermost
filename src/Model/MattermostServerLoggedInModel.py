
from .MattermostTeamModel import MattermostTeamModel

class MattermostServerLoggedInModel:
    __serverModel = None # MattermostServerModel
    __username = None
    __password = None
    __token = None

    def __init__(self, serverModel, username, password):
        if not serverModel.isReachable():
            raise Exception("Mattermost-Server %s is not reachable!" % serverModel.getUrl())

        responseHeaders, content = serverModel.callServer("POST", "/users/login", {
            'login_id': username,
            'password': password
        })

        if "token" not in responseHeaders:
            if "message" in content:
                raise Exception("Server response: %s" % content['message'])
            else:
                raise Exception("Cannot login on this server!")

        self.__serverModel = serverModel
        self.__token = responseHeaders['token']
        self.__username = username
        self.__password = password

    def createUser(self):
        raise Exception("*UNIMPLEMENTED*")
        headers, result = self.callServer("POST", "/users/create")

    def getUser(self):
        raise Exception("*UNIMPLEMENTED*")
        headers, result = self.callServer("GET", "/users/me")

    def logout(self):
        raise Exception("*UNIMPLEMENTED*")
        headers, result = self.callServer("POST", "/users/logout")

    def getUsers(self, limit=30):
        raise Exception("*UNIMPLEMENTED*")
        headers, result = self.callServer("GET", "/users/{offset}/%d" % limit)

    def searchUsers(self):
        raise Exception("*UNIMPLEMENTED*")
        headers, result = self.callServer("POST", "/users/search")

    def getUsersByIds(self):
        raise Exception("*UNIMPLEMENTED*")
        headers, result = self.callServer("POST", "/users/ids")

    def updateUser(self):
        raise Exception("*UNIMPLEMENTED*")
        headers, result = self.callServer("POST", "/users/update")

    def updateUserRoles(self):
        raise Exception("*UNIMPLEMENTED*")
        headers, result = self.callServer("POST", "/users/update_roles")

    def updateUserIsActive(self):
        raise Exception("*UNIMPLEMENTED*")
        headers, result = self.callServer("POST", "/users/update_active")

    def updateUserNotificationProperties(self):
        raise Exception("*UNIMPLEMENTED*")
        headers, result = self.callServer("POST", "/users/update_notify")

    def updateUserPassword(self):
        raise Exception("*UNIMPLEMENTED*")
        headers, result = self.callServer("POST", "/users/newpassword")

    def sendPasswordResetMail(self):
        raise Exception("*UNIMPLEMENTED*")
        headers, result = self.callServer("POST", "/users/send_password_reset")

    def getFile(self, fileId):
        raise Exception("*UNIMPLEMENTED*")
        headers, result = self.callServer("GET", "/files/%s/get" % fileId)

        return MattermostFileModel(self, fileSomething) # TODO

    def savePreferences(self):
        raise Exception("*UNIMPLEMENTED*")
        headers, result = self.callServer("POST", "/preferences/save")

    def deletePreferences(self):
        raise Exception("*UNIMPLEMENTED*")
        headers, result = self.callServer("POST", "/preferences/delete")

    def getPreferences(self, category):
        raise Exception("*UNIMPLEMENTED*")
        headers, result = self.callServer("GET", "/preferences/%s")

    def getPreference(self, category, name):
        raise Exception("*UNIMPLEMENTED*")
        headers, result = self.callServer("GET", "/preferences/%s/%s" % (category, name))

    def createTeam(self):
        raise Exception("*UNIMPLEMENTED*")
        headers, result = self.callServer("POST", "/teams/create")

        return MattermostTeamModel(self, teamName) # TODO

    def getAllTeams(self):
        headers, teams = self.callServer("GET", "/teams/all")
        teamModels = []
        for teamId in teams:
            teamData = teams[teamId]
            teamModel = MattermostTeamModel.fromJsonTeamObject(self, teamData)
            teamModels.append(teamModel)
        return teamModels

    def teamExists(self, teamName):
        foundTeam = False
        teams = self.getAllTeams()
        for teamCandidate in teams:
            if teamCandidate.getName() == teamName:
                foundTeam = True
                break
        return foundTeam

    def getTeam(self, teamName):
        team = None
        teams = self.getAllTeams()
        for teamCandidate in teams:
            if teamCandidate.getName() == teamName:
                team = teamCandidate
                break
        if team == None:
            raise Exception("Team %s does not exist or is not accessable for this user!" % teamName)
        return team

    def callServer(self, method, route, data=None, headers={}):
        headers['Authorization'] = "Bearer " + self.__token
        return self.__serverModel.callServer(method, route, data, headers)
