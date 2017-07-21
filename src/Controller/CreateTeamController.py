
from gi.repository import Gtk

class CreateTeamController:
    __gladeBuilder = None           # Gtk.Builder
    __application = None            # Application
    __window = None                 # Gtk.Window
    __teamModel = None              # Mattermost.TeamModel
    __channelType = "channel"       # string

    def __init__(self, application, teamModel, channelType="channel"):
        self.__application = application

        self.__gladeBuilder = application.createGladeBuilder('create_channel')
        self.__gladeBuilder.connect_signals(self)

        self.__window = self.__gladeBuilder.get_object('windowCreateChannel')

        self.__teamModel = teamModel
        self.__channelType = channelType

    def show(self):
        self.__window.show_all()

    def onOKClicked(self, button, data=None):
        # Gtk.Entry
        entryName = self.__gladeBuilder.get_object('entryName')

        # Gtk.TextBuffer
        textbufferPurpose = self.__gladeBuilder.get_object('textbufferPurpose')

        # Gtk.TextBuffer
        textbufferHeader = self.__gladeBuilder.get_object('textbufferHeader')

        # string
        channelName = entryName.get_text()

        # string
        purpose = textbufferPurpose.get_text(
            textbufferPurpose.get_start_iter(),
            textbufferPurpose.get_end_iter(),
            False
        )

        # string
        header = textbufferHeader.get_text(
            textbufferHeader.get_start_iter(),
            textbufferHeader.get_end_iter(),
            False
        )

        channelType = 'O'

        if self.__channelType == 'direct-message':
            pass

        if self.__channelType == 'private-group':
            channelType = 'P'

        try:
            # Mattermost.ChannelModel
            channel = self.__teamModel.createChannel(
                channelName,
                channelType=channelType
                purpose=purpose,
                header=header
            )

            self.__window.hide()

        except Exception as exception:
            dialog = Gtk.Dialog(
                "Error while creating chennel %s" % (channelName, ),
                self.__window,
                0,
                (Gtk.STOCK_OK, Gtk.ResponseType.OK)
            )
            dialog.get_content_area().add(Gtk.Label(str(exception)))
            dialog.show_all()
            dialog.run()
            dialog.destroy()

    def onCancelClicked(self, button, data=None):
        self.__window.hide()
