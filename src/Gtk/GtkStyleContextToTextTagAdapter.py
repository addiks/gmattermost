
from gi.repository import Gtk

# This component allows applying style-properties from (css-)style-providers to text-tag's.
class GtkStyleProviderToTextTagAdapter:
    __styleProvider = None # Gtk.StyleProvider

    def __init__(self, styleProvider):
        # Gtk.StyleProvider

        self.__styleProvider = styleProvider

    def attachTextTag(self, textTag, textView, classes=[]):
        # Gtk.TextTag, Gtk.TextView

        # Gtk.StyleProvider
        styleProvider = self.__styleProvider

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

    def __buildWidgetPathForTextTag(textTag, textView, classes=[]):
        # Gtk.TextTag, Gtk.TextView

        # Gtk.WidgetPath
        widgetPath = textView.get_widget_path()

        textTagPos = widgetPath.append_type(Gtk.TextTag)

        widgetPath.iter_set_name(textTagPos, textTag.name)

        for className in classes:
            widgetPath.iter_add_class(textTagPos, className)

        return widgetPath
