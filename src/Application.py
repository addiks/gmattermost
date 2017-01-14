
import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gio, Gtk
from os.path import dirname
import os

from .Controller.TeamsListController import TeamsListController
from .Model.ProfileModel import ProfileModel
from .Model.MattermostServerModel import MattermostServerModel

class Application(Gtk.Application):
    __assetPath = None
    __profileModel = None
    __servers = {}

    def __init__(self):
        Gtk.Application.__init__(
            self,
            application_id="de.addiks.gmattermost",
            flags=Gio.ApplicationFlags.FLAGS_NONE
        )
        self.connect("activate", self.onActivate)

        assetPath = dirname(dirname(__file__)) + "/assets/"

        profilePath = os.path.expanduser("~/.local/share/gmattermost/profile.xml")

        self.__profileModel = ProfileModel(profilePath)
        self.__assetPath = assetPath

    def onActivate(self, app):
        profile = self.__profileModel

        if profile.getShowOnStartup() or True:
            controller = TeamsListController(self)
            controller.run()

    def getAssetPath(self):
        return self.__assetPath

    def getProfileModel(self):
        return self.__profileModel

    def getServerModel(self, url):
        if url not in self.__servers:
            self.__servers[url] = MattermostServerModel(url)
        return self.__servers[url]

    def createGladeBuilder(self, name):
        assetPath = self.__assetPath

        gladeFilePath = assetPath + "glade/" + name + ".glade"

        gladeBuilder = Gtk.Builder()
        gladeBuilder.add_from_file(gladeFilePath)

        return gladeBuilder
