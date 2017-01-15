
class TeamController:
    __gladeBuilder = None # Gtk.Builder
    __application = None  # Application
    __window = None       # Gtk.Window
    __serverModel = None  # MattermostServerModel

    def __init__(self, application, url, username, password, teamName):
        self.__application = application
        self.__gladeBuilder = application.createGladeBuilder('team')

        self.__window = gladeBuilder.get_object('windowTeam')

        self.__serverModel = MattermostServerModel(url)
        self.__serverModel.login(username, password)
        self.__serverModel.selectTeam(teamName)

    def show(self):
        self.__window.show_all()
