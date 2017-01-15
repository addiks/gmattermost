
from gi.repository import Gio, Gtk
import re

class EditTeamController:
    __application = None    # Application
    __gladeBuilder = None   # Gtk.Builder
    __submitCallback = None # function
    __window = None         # Gtk.Window

    def __init__(self, application, submitCallback, url="", username="", password="", team=""):
        self.__application = application
        self.__submitCallback = submitCallback

        self.__gladeBuilder = application.createGladeBuilder("edit_team")
        self.__gladeBuilder.connect_signals(self)

        self.__window = self.__gladeBuilder.get_object('windowEditTeam')

        # Gtk.Entry
        urlInput = self.__gladeBuilder.get_object('entryEditTeamURL')
        urlInput.set_text(url)

        # Gtk.Entry
        teamInput = self.__gladeBuilder.get_object('entryEditTeamTeam')
        teamInput.set_text(team)

        # Gtk.Entry
        usernameInput = self.__gladeBuilder.get_object('entryEditTeamUsername')
        usernameInput.set_text(username)

        # Gtk.Entry
        passwordInput = self.__gladeBuilder.get_object('entryEditTeamPassword')
        passwordInput.set_text(password)

    def show(self):
        self.__window.show_all()

    def onSubmitButtonClicked(self, button, data=None):

        # Gtk.Entry
        urlInput = self.__gladeBuilder.get_object('entryEditTeamURL')

        # Gtk.Entry
        teamInput = self.__gladeBuilder.get_object('entryEditTeamTeam')

        # Gtk.Entry
        usernameInput = self.__gladeBuilder.get_object('entryEditTeamUsername')

        # Gtk.Entry
        passwordInput = self.__gladeBuilder.get_object('entryEditTeamPassword')

        url = urlInput.get_text()
        team = teamInput.get_text()
        username = usernameInput.get_text()
        password = passwordInput.get_text()

        self.__window.close()

        self.__submitCallback(url, team, username, password)

    def onEntriesChanged(self, entry, data=None):
        # Gtk.Builder
        gladeBuilder = self.__gladeBuilder

        # Gtk.Label
        urlCheckLabel = gladeBuilder.get_object('labelEditTeamCheckURL')

        # Gtk.Label
        teamCheckLabel = gladeBuilder.get_object('labelEditTeamCheckTeam')

        # Gtk.Label
        usernameCheckLabel = gladeBuilder.get_object('labelEditTeamCheckUsername')

        # Gtk.Label
        passwordCheckLabel = gladeBuilder.get_object('labelEditTeamCheckPassword')

        urlCheckLabel.set_text('')
        teamCheckLabel.set_text('')
        usernameCheckLabel.set_text('')
        passwordCheckLabel.set_text('')

        ### VALIDATE URL

        # Gtk.Entry
        urlInput = gladeBuilder.get_object('entryEditTeamURL')

        url = urlInput.get_text()

        if len(url) <= 0:
            return

        if re.match('^[a-zA-Z0-9]+\:\/\/[a-zA-Z0-9_-]', url) is None:
            urlCheckLabel.set_text('URL must be like "protocol://hostname/path/"')
            return

        server = self.__application.getServerModel(url)

        if not server.isReachable():
            urlCheckLabel.set_text('This URL does not respond!')
            return

        urlCheckLabel.set_text('OK')

        ### VALIDATE USERNAME

        # Gtk.Entry
        usernameInput = gladeBuilder.get_object('entryEditTeamUsername')

        username = usernameInput.get_text()

        if len(username) <= 0:
            return

        usernameCheckLabel.set_text('OK')

        ### VALIDATE PASSWORD

        # Gtk.Entry
        passwordInput = gladeBuilder.get_object('entryEditTeamPassword')

        password = passwordInput.get_text()

        if len(password) <= 0:
            return

        passwordCheckLabel.set_text('OK')

        ### VALIDATE TEAM NAME

        # Gtk.Entry
        teamInput = gladeBuilder.get_object('entryEditTeamTeam')

        team = teamInput.get_text()

        if len(team) <= 0:
            return

        teamCheckLabel.set_text('OK')

    def onValidateLogin(self, button, data=None):

        # Gtk.Builder
        gladeBuilder = self.__gladeBuilder

        # Gtk.Entry
        urlInput = gladeBuilder.get_object('entryEditTeamURL')

        url = urlInput.get_text()

        if len(url) <= 0:
            return

        if re.match('^[a-zA-Z0-9]+\:\/\/[a-zA-Z0-9_-]', url) is None:
            urlCheckLabel.set_text('URL must be like "protocol://hostname/path/"')
            return

        server = self.__application.getServerModel(url)

        # Gtk.Entry
        usernameInput = gladeBuilder.get_object('entryEditTeamUsername')

        username = usernameInput.get_text()

        # Gtk.Entry
        passwordInput = gladeBuilder.get_object('entryEditTeamPassword')

        password = passwordInput.get_text()

        # Gtk.Entry
        teamInput = gladeBuilder.get_object('entryEditTeamTeam')

        teamName = teamInput.get_text()

        server = self.__application.getServerModel(url)

        checkConnectionLabel = gladeBuilder.get_object('labelEditTeamCheckConnection')

        try:
            server.login(username, password)

            teams = server.listTeams()

            foundTeam = False
            for teamId in teams:
                if teams[teamId]['display_name'] == teamName:
                    foundTeam = True
            if not foundTeam:
                raise Exception("Team '%s' not found or accassible to you!" % teamName)

            dialog = Gtk.Dialog(
                "Success!",
                self.__window,
                0,
                (Gtk.STOCK_OK, Gtk.ResponseType.OK)
            )
            dialog.get_content_area().add(Gtk.Label("Login was successful!"))

        except Exception as exception:
            dialog = Gtk.Dialog(
                "Error while testing connection",
                self.__window,
                0,
                (Gtk.STOCK_OK, Gtk.ResponseType.OK)
            )
            dialog.get_content_area().add(Gtk.Label(str(exception)))

        if type(dialog) == Gtk.Dialog:
            dialog.show_all()
            dialog.run()
            dialog.destroy()
