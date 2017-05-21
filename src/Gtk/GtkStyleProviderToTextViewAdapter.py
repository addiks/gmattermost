
from copy import copy
from gi.repository import Gtk

# This component allows applying style-properties from (css-)style-providers to text-tag's.
class GtkStyleProviderToTextViewAdapter:
    __styleProvider = None   # Gtk.StyleProvider
    __attachedTextViews = [] # list(Gtk.TextView)
    __ignoreEvents = False   # boolean

    def __init__(self, styleProvider):
        # Gtk.StyleProvider

        self.__styleProvider = styleProvider

    def attachTextView(self, textView):
        # Gtk.TextView

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

        # Gtk.StyleProvider
        styleProvider = self.__styleProvider

        # Gtk.WidgetPath
        widgetPath = self.__buildWidgetPathForTextTag(textTag, textView)

        styleContext = Gtk.StyleContext()
        styleContext.set_path(widgetPath)
        styleContext.add_provider(styleProvider, 800)
        #styleContext.invalidate() # Deprecated (?)

        for prop in textTag.list_properties():
            # GParamString

            cssPropertyName = self.__mapTextTagPropertyNameToCSSName(prop.name)

            if cssPropertyName != None:
                cssPropertyValue = styleContext.get_property(cssPropertyName, styleContext.get_state())

                if cssPropertyValue != None:
                    self.__ignoreEvents = True
                    textTag.set_property(prop.name, cssPropertyValue)
                    self.__ignoreEvents = False

    def __onTagAddedToTagTable(self, tagTable, textTag, data=None):
        if not self.__ignoreEvents:
            for textView in self.__attachedTextViews:
                # Gtk.TextView

                # Gtk.TextBuffer
                textBuffer = textView.get_buffer()

                if textBuffer.get_tag_table() == tagTable:
                    self.__updateTextTag(textTag, textView)

    def __onTagChangedInTagTable(self, tagTable, textTag, sizeChanged, data=None):
        if not self.__ignoreEvents:
            for textView in self.__attachedTextViews:
                # Gtk.TextView

                # Gtk.TextBuffer
                textBuffer = textView.get_buffer()

                if textBuffer.get_tag_table() == tagTable:
                    self.__updateTextTag(textTag, textView)

    def __onTagRemovedFromTagTable(self, tagTable, textTag, data=None):
        if not self.__ignoreEvents:
            pass

    def __buildWidgetPathForTextTag(self, textTag, textView):
        # Gtk.TextTag, Gtk.TextView

        # Gtk.WidgetPath
        widgetPath = textView.get_path().copy()

        textTagPos = widgetPath.append_type(Gtk.TextTag)

        tagName = textTag.get_property('name')
        tagClasses = tagName.split("_")

        widgetPath.iter_set_name(textTagPos, tagName)

        for className in tagClasses:
            widgetPath.iter_add_class(textTagPos, className)

        return widgetPath

    def __mapTextTagPropertyNameToCSSName(self, name):
        result = None
        nameMap = {
            'accumulative-margin': None,
            'background': None,
            'background-full-height': None,
            'background-full-height-set': None,
            'background-gdk': None,
            'background-rgba': None,
            'background-set': None,
            'direction': None,
            'editable': None,
            'editable-set': None,
            'fallback': None,
            'fallback-set': None,
            'family': None,
            'family-set': None,
            'font': None,
            'font-desc': None,
            'font-features': None,
            'font-features-set': None,
            'foreground': None,
            'foreground-gdk': None,
            'foreground-rgba': None,
            'foreground-set': None,
            'indent': None,
            'indent-set': None,
            'invisible': None,
            'invisible-set': None,
            'justification': None,
            'justification-set': None,
            'language': None,
            'language-set': None,
            'left-margin': None,
            'left-margin-set': None,
            'letter-spacing': None,
            'letter-spacing-set': None,
            'name': None,
            'paragraph-background': None,
            'paragraph-background-gdk': None,
            'paragraph-background-rgba': None,
            'paragraph-background-set': None,
            'pixels-above-lines': None,
            'pixels-above-lines-set': None,
            'pixels-below-lines': None,
            'pixels-below-lines-set': None,
            'pixels-inside-wrap': None,
            'pixels-inside-wrap-set': None,
            'right-margin': None,
            'right-margin-set': None,
            'rise': None,
            'rise-set': None,
            'scale': None,
            'scale-set': None,
            'size': None,
            'size-points': None,
            'size-set': None,
            'stretch': None,
            'stretch-set': None,
            'strikethrough': None,
            'strikethrough-rgba': None,
            'strikethrough-rgba-set': None,
            'strikethrough-set': None,
            'style': None,
            'style-set': None,
            'tabs': None,
            'tabs-set': None,
            'underline': None,
            'underline-rgba': None,
            'underline-rgba-set': None,
            'underline-set': None,
            'variant': None,
            'variant-set': None,
            'weight': 'font-weight',
            'weight-set': None,
            'wrap-mode': None,
            'wrap-mode-set': None
        }
        if name in nameMap:
            result = nameMap[name]
        return result
