
import httplib2
import json

# https://api.mattermost.com/

class MattermostServerModel:
    __http = None
    __url = None
    __token = None
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

    def listTeams(self):
        pass

    def login(self, username, password):

        if not self.isReachable():
            raise Exception("Mattermost-Server %s is not reachable!" % self.__url)

        url = self.__url + "/api/v3/users/login"

        print("A")
        print(json.dumps({
            'login_id': username,
            'password': password
        }))

        responseHeaders, contentJson = self.__http.request(url, "POST", body=json.dumps({
            'login_id': username,
            'password': password
        }))

        if type(contentJson) == bytes:
            contentJson = contentJson.decode()

        content = json.loads(contentJson)

        print(content)
        print(responseHeaders)

        if "token" in responseHeaders:
            self.__token = responseHeaders['token']

        elif "message" in content:
            raise Exception("Server response: %s" % content['message'])

        else:
            raise Exception("Cannot login on this server!")
