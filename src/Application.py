
import gi
gi.require_version('Notify', '0.7')

from gi.repository import Gio, Gtk, Notify
from os.path import dirname
import os

from .Controller.TeamsListController import TeamsListController
from .Controller.IndicatorController import IndicatorController
from .Model.ProfileModel import ProfileModel
from .Model.CacheModel import CacheModel
from Mattermost.ServerModel import ServerModel

class Application(Gtk.Application):
    __profileModel = None # ProfileModel
    __cacheModel = None # CacheModel
    __indicatorController = None # IndicatorController
    __assetPath = None
    __servers = {}

    def __init__(self):
        Gtk.Application.__init__(
            self,
            application_id="de.addiks.gmattermost",
            flags=Gio.ApplicationFlags.FLAGS_NONE
        )
        self.connect("activate", self.onActivate)

        Notify.init("gmattermost")

        assetPath = dirname(dirname(__file__)) + "/assets/"

        profilePath = os.path.expanduser("~/.local/share/gmattermost/profile.xml")
        profileModel = ProfileModel(profilePath)

        cacheDir = os.path.expanduser("~/.local/share/gmattermost/cache/")
        cacheModel = CacheModel(cacheDir)

        self.__cacheModel = cacheModel
        self.__profileModel = profileModel
        self.__assetPath = assetPath
        self.__indicatorController = IndicatorController(self)

        self.hold()

    def shutdown(self):
        self.release()

    def onActivate(self, app):
        profile = self.__profileModel

        if profile.getShowOnStartup() or True:
            self.showTeamsListWindow()

    def showTeamsListWindow(self, force=False, doStartup=True):
        teamsController = TeamsListController(self)
        teamsController.show(force, doStartup)

    def getAssetPath(self):
        return self.__assetPath

    def getProfileModel(self):
        return self.__profileModel

    def getServerModel(self, url):
        if url not in self.__servers:
            self.__servers[url] = ServerModel(url)
        return self.__servers[url]

    def getCache(self, cacheKey):
        cacheModel = self.__cacheModel
        return cacheModel.get(cacheKey)

    def putCache(self, cacheKey, content):
        cacheModel = self.__cacheModel
        cacheModel.put(cacheKey, content)

    def getCacheFilePath(self, cacheKey):
        cacheModel = self.__cacheModel
        return cacheModel.getCacheFilePath(cacheKey)

    def createGladeBuilder(self, name):
        assetPath = self.__assetPath

        gladeFilePath = assetPath + "glade/" + name + ".glade"

        gladeBuilder = Gtk.Builder()
        gladeBuilder.add_from_file(gladeFilePath)

        return gladeBuilder

    def createStyleProvider(self, name):
        assetPath = self.__assetPath

        cssFilePath = assetPath + "styles/" + name + ".css"

        cssFile = Gio.File.new_for_path(cssFilePath)

        cssProvider = Gtk.CssProvider()
        cssProvider.load_from_file(cssFile)

        return cssProvider
