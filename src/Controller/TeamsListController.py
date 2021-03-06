
from gi.repository import Gtk

from .EditTeamController import EditTeamController
from .TeamController import TeamController

class TeamsListController:
    __application = None   # Application
    __gladeBuilder = None  # Gtk.Builder
    __window = None        # Gtk.Window
    __teamControllers = {} # dict(TeamController)

    def __init__(self, application):
        self.__application = application

        # Gtk.Builder
        self.__gladeBuilder = application.createGladeBuilder("teams_list")
        self.__gladeBuilder.connect_signals(self)

        self.__window = self.__gladeBuilder.get_object('windowMain')

        self.__rebuildTeamsList()

    def onWindowDestroy(self, event, data=None):
        self.__application.resetTeamsListWindow()

    def onTeamsTreeViewButtonPress(self, treeView, event, data=None):
        if event.button == 3: # right click
            # Gtk.Menu
            menu = self.__gladeBuilder.get_object('menuMainTeamContextMenu')
            menu.show_all()
            menu.popup(None, None, None, None, event.button, event.time)

    def onTeamAddButtonClicked(self, button, data=None):
        login = EditTeamController(self.__application, self.onAddTeamSubmitted)
        login.show()

    def onAddTeamSubmitted(self, url, team, username, password):
        # ProfileModel
        profile = self.__application.getProfileModel()

        profile.addTeam(url, team, username, password)

        self.__rebuildTeamsList()

    def onTeamConnectItemActivate(self, menuItem, data=None):
        # Gtk.TreeSelection
        teamsSelection = self.__gladeBuilder.get_object('treeviewSelectionMainTeams')

        # Gtk.TreeModel
        treeModel, selectedTreePaths = teamsSelection.get_selected_rows()

        for treePath in selectedTreePaths:
            # Gtk.TreeRowReference

            # Gtk.TreeIter
            treeIter = treeModel.get_iter(treePath)

            url = treeModel.get_value(treeIter, 0)
            username = treeModel.get_value(treeIter, 1)
            teamName = treeModel.get_value(treeIter, 3)
            password = treeModel.get_value(treeIter, 4)

            try:
                teamController = TeamController(
                    self.__application,
                    url,
                    username,
                    password,
                    teamName
                )
                teamController.show()

            except Exception as exception:
                dialog = Gtk.Dialog(
                    "Error while connecting to %s - %s as %s" % (url, teamName, username),
                    self.__window,
                    0,
                    (Gtk.STOCK_OK, Gtk.ResponseType.OK)
                )
                dialog.get_content_area().add(Gtk.Label(str(exception)))
                dialog.show_all()
                dialog.run()
                dialog.destroy()

    def onTeamEditItemActivate(self, menuItem, data=None):
        # Gtk.TreeSelection
        teamsSelection = self.__gladeBuilder.get_object('treeviewSelectionMainTeams')

        # Gtk.TreeModel
        treeModel, selectedTreePaths = teamsSelection.get_selected_rows()

        for treePath in selectedTreePaths:
            # Gtk.TreeRowReference

            # Gtk.TreeIter
            treeIter = treeModel.get_iter(treePath)

            url = treeModel.get_value(treeIter, 0)
            username = treeModel.get_value(treeIter, 1)
            teamName = treeModel.get_value(treeIter, 3)
            password = treeModel.get_value(treeIter, 4)

            print([url, username, password, teamName])

            login = EditTeamController(
                self.__application,
                self.onEditTeamSubmitted,
                str(url),
                str(username),
                str(password),
                str(teamName)
            )
            login.run()

    def onEditTeamSubmitted(self, url, team, username, password):
        # ProfileModel
        profile = self.__application.getProfileModel()

        profile.removeTeam(url, team, username)
        profile.addTeam(url, team, username, password)

        self.__rebuildTeamsList()

    def onTeamDeleteItemActivate(self, menuItem, data=None):
        # ProfileModel
        profile = self.__application.getProfileModel()

        # Gtk.TreeSelection
        teamsSelection = self.__gladeBuilder.get_object('treeviewSelectionMainTeams')

        # Gtk.TreeModel
        teamsListstore, selectedTreePaths = teamsSelection.get_selected_rows()

        for treePath in selectedTreePaths:
            # Gtk.TreeRowReference

            # Gtk.TreeIter
            treeIter = teamsListstore.get_iter(treePath)

            url = teamsListstore.get_value(treeIter, 0)
            username = teamsListstore.get_value(treeIter, 1)
            teamName = teamsListstore.get_value(treeIter, 3)

            profile.removeTeam(url, teamName, username)

        self.__rebuildTeamsList()

    def onShowOnStartupClicked(self, checkbox, data=None):
        # ProfileModel
        profile = self.__application.getProfileModel()
        profile.setShowOnStartup(checkbox.get_active())

    def onConnectTeamOnStartupToggled(self, cellRenderer, treePath, data=None):
        # Gtk.ListStore
        teamsListstore = self.__gladeBuilder.get_object('liststoreMainTeams')

        # ProfileModel
        profile = self.__application.getProfileModel()

        # Gtk.TreeIter
        treeIter = teamsListstore.get_iter(treePath)

        url = teamsListstore.get_value(treeIter, 0)
        username = teamsListstore.get_value(treeIter, 1)
        doesConnectOnStartup = teamsListstore.get_value(treeIter, 2)
        teamName = teamsListstore.get_value(treeIter, 3)

        doesConnectOnStartup = not doesConnectOnStartup

        teamsListstore.set_value(treeIter, 2, doesConnectOnStartup)
        profile.setConnectTeamOnStartup(url, teamName, username, doesConnectOnStartup)

    def show(self, force=False, doStartup=True):
        # ProfileModel
        profile = self.__application.getProfileModel()

        if profile.getShowOnStartup() or force:
            self.__window.show_all()
            self.__window.present()

        if doStartup:
            for team in profile.getTeams():
                if team['open-on-startup']:
                    try:
                        teamKey = team['username'] + ":" + team['password'] + "@" + team['url']
                        if teamKey not in self.__teamControllers:
                            self.__teamControllers[teamKey] = TeamController(
                                self.__application,
                                team['url'],
                                team['username'],
                                team['password'],
                                team['team']
                            )
                        self.__teamControllers[teamKey].show()

                    except Exception as exception:
                        dialog = Gtk.Dialog(
                            "Error while connecting to %s - %s as %s" % (team['url'], team['team'], team['username']),
                            self.__window,
                            0,
                            (Gtk.STOCK_OK, Gtk.ResponseType.OK)
                        )
                        dialog.get_content_area().add(Gtk.Label(str(exception)))
                        dialog.show_all()
                        dialog.run()
                        dialog.destroy()

    def __rebuildTeamsList(self):
        # ProfileModel
        profile = self.__application.getProfileModel()

        # Gtk.CheckButton
        showOnStartCheckbox = self.__gladeBuilder.get_object('checkbuttonMainHeaderShowOnStartup')

        showOnStartCheckbox.set_active(profile.getShowOnStartup())

        # Gtk.ListStore
        teamsListstore = self.__gladeBuilder.get_object('liststoreMainTeams')

        teamsListstore.clear()

        for team in profile.getTeams():
            # Gtk.TreeIter
            treeIter = teamsListstore.append()

            teamsListstore.set_value(treeIter, 0, team['url'])
            teamsListstore.set_value(treeIter, 1, team['username'])
            teamsListstore.set_value(treeIter, 2, team['open-on-startup'])
            teamsListstore.set_value(treeIter, 3, team['team'])
            teamsListstore.set_value(treeIter, 4, team['password'])
