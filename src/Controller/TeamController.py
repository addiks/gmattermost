
class TeamController:
    __gladeBuilder = None # Gtk.Builder
    __application = None  # Application
    __window = None       # Gtk.Window

    def __init__(self, application):
        self.__application = application
        self.__gladeBuilder = application.createGladeBuilder()

        self.__window = gladeBuilder.get_object('windowTeam')

    def run(self):
        self.__window.show_all()
