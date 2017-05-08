
import asyncio
import websockets
import json
import uuid

from _thread import start_new_thread

from .TeamModel import TeamModel
from .UserModel import UserModel

class ServerLoggedInModel:
    __serverModel = None      # ServerModel
    __selfUser = None         # UserModel
    __webSocket = None        # websocket
    __webSocketSeq = 0        # integer
    __webSocketCallbacks = {} # callback[]
    __eventListener = {}      # callback[]
    __userCache = {}
    __username = None
    __password = None
    __token = None
    __isStopping = False      # boolean

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

        asyncio.get_event_loop().run_until_complete(self.__connectWebsocket())

        self.sendWebsocketRequest("authentication_challenge", {
            'token': self.__token
        })

        start_new_thread(asyncio.get_event_loop().run_until_complete, (self.__handleWebsocket(), ))

    async def __connectWebsocket(self):
        # ServerModel
        server = self.__serverModel

        scheme = server.getUrlScheme()
        hostname = server.getUrlHostname()
        port = server.getUrlPort()
        path = server.getUrlPath()

        webSocketScheme = 'ws'
        if scheme == "https":
            webSocketScheme = 'wss'

        portStr = ""
        if port != None:
            portStr = ":" + str(port)

        url = webSocketScheme + '://' + hostname + portStr + path + "/api/v3/users/websocket"

        print(url)

        webSocket = await websockets.connect(url)
        self.__webSocket = webSocket

    async def __handleWebsocket(self):
        # websockets.client.WebSocketClientProtocol
        webSocket = self.__webSocket

        while not self.__isStopping:
            messageJson = await webSocket.recv()

            print("per WS received: " + messageJson)

            message = json.loads(messageJson)

            if "seq_reply" in message:
                seqNo = str(message["seq_reply"])
                if seqNo in self.__webSocketCallbacks:
                    errorObject = None
                    if "error" in message:
                        errorObject = message["error"]
                    start_new_thread(self.__webSocketCallbacks[seqNo], (message['status'], errorObject))

            if "event" in message:
                eventName = str(message["event"])
                eventData = message["data"]

                # TODO: handle broadcase-info (https://api.mattermost.com/v3.7/#tag/WebSocket)
                #  "broadcast":{ # info about who this event was sent to
                #    "omit_users": null,
                #    "user_id": "ay5sq51sebfh58ktrce5ijtcwy",
                #    "channel_id": "",
                #    "team_id": ""
                #  }

                if eventName in self.__eventListener:
                    broadcast = message["broadcast"]
                    for broadcastFilter, callback in self.__eventListener[eventName]:
                        if broadcastFilter == None:
                            start_new_thread(callback, (eventData, ))
                        else:
                            matches = True
                            for broadcastKey in broadcastFilter:
                                broadcastValue = broadcastFilter[broadcastKey]
                                if broadcastValue != broadcast[broadcastKey]:
                                    matches = False
                                    break
                            if matches:
                                start_new_thread(callback, (eventData, ))

        webSocket.close()

    def registerNewUserListener(self, callback):
        self.registerEventListener("new_user", callback)

    def registerLeaveTeamListener(self, callback):
        self.registerEventListener("leave_team", callback)

    def registerUserAddedListener(self, callback):
        self.registerEventListener("user_added", callback)

    def registerUserUpdatedListener(self, callback):
        self.registerEventListener("user_updated", callback)

    def registerUserRemovedListener(self, callback):
        self.registerEventListener("user_removed", callback)

    def registerPreferenceChangedListener(self, callback):
        self.registerEventListener("preference_changed", callback)

    def registerEphemeralMessageListener(self, callback):
        self.registerEventListener("ephemeral_message", callback)

    def registerStatusChangeListener(self, callback):
        self.registerEventListener("status_change", callback)

    def registerHelloListener(self, callback):
        self.registerEventListener("hello", callback)

    def registerWebRTCListener(self, callback):
        self.registerEventListener("webrtc", callback)

    def requestStatuses(self, callback):
        self.sendWebsocketRequest("get_statuses", responseCallback=callback)

    def requestStatusesById(self, idList, callServer):
        self.sendWebsocketRequest("get_statuses_by_ids", idList, callback)
        # TODO: confirm that this is correct

    def registerEventListener(self, eventName, callback, broadcast=None):
        eventName = str(eventName)
        if eventName not in self.__eventListener:
            self.__eventListener[eventName] = []
        self.__eventListener[eventName].append([broadcast, callback])

    def sendWebsocketRequest(self, actionName, payloadData={}, responseCallback=None):
        self.__webSocketSeq += 1

        seqNo = str(self.__webSocketSeq)

        if responseCallback != None:
            self.__webSocketCallbacks[seqNo] = responseCallback

        data = {
            'seq': self.__webSocketSeq,
            'action': str(actionName),
            'data': payloadData
        }

        dataJson = json.dumps(data)

        result = self.__webSocket.send(dataJson)

        print(result)

        asyncio.get_event_loop().run_until_complete(result)

        print("per WS sent: " + dataJson)

    def logout(self):
        self.__isStopping = True
        # TODO send logout REST request

    def createUser(self):
        raise Exception("*UNIMPLEMENTED*")
        headers, result = self.callServer("POST", "/users/create")

    def getSelfUser(self):
        if self.__selfUser == None:
            headers, result = self.callServer("GET", "/users/me")
            self.__selfUser = UserModel.fromJsonUserObject(result, self)
        return self.__selfUser

    def logout(self):
        raise Exception("*UNIMPLEMENTED*")
        headers, result = self.callServer("POST", "/users/logout")

    def getUsers(self, limit=30):
        raise Exception("*UNIMPLEMENTED*")
        headers, result = self.callServer("GET", "/users/{offset}/%d" % limit)

    def searchUsers(self):
        raise Exception("*UNIMPLEMENTED*")
        headers, result = self.callServer("POST", "/users/search")

    def getUsersByIds(self, userIds):
        users = []
        print(userIds)
        userIdsToFetch = []
        for userId in userIds:
            if userId in self.__userCache:
                users.append(self.__userCache[userId])
            else:
                userIdsToFetch.append(userId)

        if len(userIdsToFetch) > 0:
            headers, result = self.callServer("POST", "/users/ids", userIdsToFetch)

            for userId in result:
                userJsonData = result[userId]
                user = UserModel.fromJsonUserObject(userJsonData, self)
                users.append(user)
                self.__userCache[userId] = user

        return users

    def getUserById(self, userId):
        user = None
        users = self.getUsersByIds([userId])
        if len(users) > 0:
            user = users[0]
        return user

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

    def getUserImage(self, userId, lastPictureUpdate):
        imageData = None
        if lastPictureUpdate != None:
            url = "/users/%s/image?time=%d" % (userId, lastPictureUpdate)
            headers, imageData = self.callServer("GET", url, returnPlainResponse=True)
        return imageData

    def getFile(self, fileId):
        raise Exception("*UNIMPLEMENTED*")
        headers, result = self.callServer("GET", "/files/%s/get" % fileId)

        return FileModel(self, fileSomething) # TODO

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

        return TeamModel(self, teamName) # TODO

    def getAllTeams(self):
        headers, teams = self.callServer("GET", "/teams/all")
        teamModels = []
        for teamId in teams:
            teamData = teams[teamId]
            teamModel = TeamModel.fromJsonTeamObject(self, teamData)
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

    def createId(self):
        return str(uuid.uuid4())

    def callServer(self, method, route, data=None, headers={}, version="v3", returnPlainResponse=False):
        print("Token: " + str(self.__token))
        headers['Authorization'] = "Bearer " + self.__token
        return self.__serverModel.callServer(method, route, data, headers, version, returnPlainResponse)
