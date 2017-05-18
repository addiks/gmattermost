
from copy import copy
from gi.repository import Gtk

# This component allows applying style-properties from (css-)style-providers to text-tag's.
class GtkStyleProviderToTextViewAdapter:
    __styleProvider = None   # Gtk.StyleProvider
    __attachedTextViews = [] # list(Gtk.TextView)

    def __init__(self, styleProvider):
        # Gtk.StyleProvider

        self.__styleProvider = styleProvider

    def attachTextView(self, textView):
        # Gtk.TextView

        # Gtk.StyleProvider
        styleProvider = self.__styleProvider

        if textView not in self.__attachedTextViews:
            self.__attachedTextViews.append(textView)

            # Gtk.TextBuffer
            textBuffer = textView.get_buffer()

            # Gtk.TagTable
            tagTable = textBuffer.get_tag_table()

            tagTable.connect('tag-added',   self.__onTagAddedToTagTable)
            tagTable.connect('tag-changed', self.__onTagChangedInTagTable)
            tagTable.connect('tag-removed', self.__onTagRemovedFromTagTable)

            tagTable.foreach(self.__updateTextTag, textView)

    def __updateTextTag(self, textTag, textView):
        # Gtk.TextTag, Gtk.TextView

        # Gtk.WidgetPath
        widgetPath = self.__buildWidgetPathForTextTag(textTag, textView)

        styleContext = Gtk.StyleContext()
        styleContext.add_provider(styleProvider)
        styleContext.set_path(widgetPath)
        #styleContext.invalidate() # Deprecated (?)

        for prop in textTag.list_properties():
            # GParamString

            cssPropertyValue = styleContext.get_property(prop.name)

            if cssPropertyValue != None:
                textTag.set_property(prop.name, cssPropertyValue)

    def __onTagAddedToTagTable(self, tagTable, textTag, data=None):
        for textView in self.__attachedTextViews:
            if textView.get_tag_table() == tagTable:
                self.__updateTextTag(textTag, textView)

    def __onTagChangedInTagTable(self, tagTable, textTag, sizeChanged, data=None):
        for textView in self.__attachedTextViews:
            if textView.get_tag_table() == tagTable:
                self.__updateTextTag(textTag, textView)

    def __onTagRemovedFromTagTable(self, tagTable, textTag, data=None):
        pass

    def __buildWidgetPathForTextTag(textTag, textView):
        # Gtk.TextTag, Gtk.TextView

        # Gtk.WidgetPath
        widgetPath = copy(textView.get_path())

        textTagPos = widgetPath.append_type(Gtk.TextTag)

        widgetPath.iter_set_name(textTagPos, textTag.name)

        if hasattr(textTag, 'classes'):
            for className in textTag.classes:
                widgetPath.iter_add_class(textTagPos, className)

        return widgetPath
