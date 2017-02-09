


class TeamController:
    __gladeBuilder = None  # Gtk.Builder
    __application = None   # Application
    __window = None        # Gtk.Window
    __serverModel = None   # MattermostServerModel
    __loggedInModel = None # MattermostServerLoggedInModel
    __teamModel = None     # MattermostTeamModel

    def __init__(self, application, url, username, password, teamName):
        self.__application = application

        self.__gladeBuilder = application.createGladeBuilder('team')
        self.__gladeBuilder.connect_signals(self)

        gladeBuilder = self.__gladeBuilder

        self.__window = gladeBuilder.get_object('windowTeam')

        self.__serverModel = application.getServerModel(url)

        self.__loggedInModel = self.__serverModel.login(username, password)

        self.__teamModel = self.__loggedInModel.getTeam(teamName)

        self.__reload()


    def show(self):
        self.__window.show_all()

    def __reload(self):
        # MattermostTeamModel
        teamModel = self.__teamModel

        # Gtk.Builder
        gladeBuilder = self.__gladeBuilder

        # Gtk.ListStore
        liststoreTeamChannels = gladeBuilder.get_object('liststoreTeamChannels')

        # Gtk.ListStore
        liststoreTeamPrivateGroups = gladeBuilder.get_object('liststoreTeamPrivateGroups')

        # Gtk.ListStore
        liststoreTeamDirectMessages = gladeBuilder.get_object('liststoreTeamDirectMessages')

        for channel in teamModel.getChannels():
            # MattermostChannelModel

            if channel.isOpen():
                # Gtk.TreeIter
                treeIter = liststoreTeamChannels.append()

                liststoreTeamChannels.set_value(treeIter, 0, channel.getDisplayName())
