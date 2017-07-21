
from .CreateTeamController import CreateTeamController

class SearchChannelsController:
    __gladeBuilder = None           # Gtk.Builder
    __application = None            # Application
    __window = None                 # Gtk.Window
    __teamModel = None              # Mattermost.TeamModel
    __channelType = "channel"       # string

    def __init__(self, application, teamModel, channelType="channel"):
        self.__application = application
        self.__teamModel = teamModel
        self.__channelType = channelType

        self.__gladeBuilder = application.createGladeBuilder('search_channels')
        self.__gladeBuilder.connect_signals(self)

        self.__window = self.__gladeBuilder.get_object('windowSearchChannels')

    def show(self):
        self.__window.show_all()

    def onChannelRowClicked(self, column, data=None):
        pass

    def onCreateChannelClicked(self, button, data=None):
        createChannel = CreateTeamController(self.__application, self.__teamModel, self.__channelType)
        createChannel.show()

    def onSearchEntryChanged(self, entry, data=None):
        self._reload()

    def _reload(self):
        # Gtk.SearchEntry
        searchentrySearchChannels = self.__gladeBuilder.get_object('searchentrySearchChannels')

        term = searchentrySearchChannels.get_text()

        # [Mattermost.ChannelModel]
        channels = self.__teamModel.searchMoreChannels(term)

        # Gtk.ListStore
        liststoreFoundChannels = self.__gladeBuilder.get_object('liststoreFoundChannels')

        liststoreFoundChannels.clear()

        for channel in channels:
            # Mattermost.ChannelModel

            # Gtk.TreeIter
            treeIter = liststoreFoundChannels.append()

            liststoreFoundChannels.set_value(treeIter, 0, channel.getDisplayName())
            liststoreFoundChannels.set_value(treeIter, 1, channel.getPurpose())
            liststoreFoundChannels.set_value(treeIter, 2, channel.getId())
