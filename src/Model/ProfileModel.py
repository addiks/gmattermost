
import xml.etree.ElementTree as ElementTree
import os

class ProfileModel:
    __xmlFilePath = None
    __showOnStartup = True
    __teams = []

    def __init__(self, profilePath):
        while len(profilePath)>0 and profilePath[-1] == '/':
            profilePath = profilePath[0:-1]
        self.__xmlFilePath = profilePath
        self.__load()

    def setShowOnStartup(self, isShowOnStartup=True):
        self.__showOnStartup = isShowOnStartup
        self.__save()

    def getShowOnStartup(self):
        return self.__showOnStartup

    def addTeam(self, url, team, username, password, openOnStartUp=False):
        self.__teams.append({
            'url': url,
            'team': team,
            'username': username,
            'password': password,
            'open-on-startup': openOnStartUp
        })
        self.__save()

    def removeTeam(self, url, teamName, username):
        newTeams = []
        for team in self.__teams:
            if (
                str(team['url']) != str(url) or
                str(team['team']) != str(teamName) or
                str(team['username']) != str(username)
            ):
                newTeams.append(team)
                break
        self.__teams = newTeams
        self.__save()

    def getTeams(self):
        return self.__teams

    ### INTERNALS - SAVE & LOAD

    def __load(self):
        xmlFilePath = self.__xmlFilePath

        if os.path.exists(xmlFilePath):
            with open(xmlFilePath, "r") as xmlFile:
                xmlData = xmlFile.read()
            profileXml = ElementTree.fromstring(xmlData)

            self.__showOnStartup = profileXml.get('show-on-startup') == 'true'

            for teamXml in profileXml.iter('team'):
                self.__teams.append({
                    'url': teamXml.get('url'),
                    'team': teamXml.get('name'),
                    'username': teamXml.get('username'),
                    'password': teamXml.get('password'),
                    'open-on-startup': teamXml.get('open-on-startup') == 'true'
                })

    def __save(self):
        xmlFilePath = self.__xmlFilePath

        folderPath = os.path.dirname(xmlFilePath)

        if not os.path.exists(folderPath):
            os.makedirs(folderPath)

        profileXml = ElementTree.Element('profile')

        showOnStartupString = "false"
        if self.__showOnStartup:
            showOnStartupString = "true"
        profileXml.set('show-on-startup', showOnStartupString)

        teamsXml = ElementTree.SubElement(profileXml, "teams")

        for team in self.__teams:
            teamXml = ElementTree.SubElement(teamsXml, 'team')
            teamXml.set('url', team['url'])
            teamXml.set('name', team['team'])
            teamXml.set('username', team['username'])
            teamXml.set('password', team['password'])
            teamXml.set('open-on-startup', str(team['open-on-startup']))

        xml = ElementTree.ElementTree(profileXml)
        xml.write(xmlFilePath)
