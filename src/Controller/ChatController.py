
from gi.repository import GLib, Gtk, GdkPixbuf, Notify

from Mattermost.PostModel import PostModel
from ..Gtk.GtkStyleProviderToTextViewAdapter import GtkStyleProviderToTextViewAdapter

import json
import os

class ChatController:
    __gladeBuilder = None         # Gtk.Builder
    __styleProvider = None        # Gtk.StyleProvider
    __styleTextViewAdapter = None # Gtk.GtkStyleProviderToTextViewAdapter
    __application = None          # Application
    __window = None               # Gtk.Window
    __windowTitleTemplate = None  # string
    __channelModel = None         # Mattermost.ChannelModel
    __isWindowOpen = False        # boolean
    __lastUserId = None           # string
    __sections = []               # list([name, beginMark, list(classes)])
#    __postTreeIterMap = {}       # dict(Gtk.TreeIter)

    def __init__(self, application, channelModel):
        self.__application = application
        self.__channelModel = channelModel

        channelModel.registerTypingListener(self.onTypingEvent)
        channelModel.registerPostedListener(self.onMessagePostedEvent)
        channelModel.registerPostEditedListener(self.onMessageEditedEvent)
        channelModel.registerPostDeletedListener(self.onMessageDeletedEvent)

    def __getGladeObject(self, objectId):
        # Gtk.Builder
        gladeBuilder = self.__gladeBuilder

        gtkObject = gladeBuilder.get_object(objectId)

        self.__applyStyleToGtkObject(gtkObject)

        return gtkObject

    def __applyStyleToGtkObject(self, gtkObject):
        # Gtk.Object

        if issubclass(type(gtkObject), Gtk.Widget):
            # Gtk.StyleContext
            styleContext = gtkObject.get_style_context()

            styleContext.add_provider(self.__styleProvider, 800)

        if issubclass(type(gtkObject), Gtk.Container):
            for childGtkObject in gtkObject.get_children():
                self.__applyStyleToGtkObject(childGtkObject)

    def show(self):
        if not self.__isWindowOpen:
            self.__isWindowOpen = True

            self.__styleProvider = self.__application.createStyleProvider('chat')
            self.__styleTextViewAdapter = GtkStyleProviderToTextViewAdapter(self.__styleProvider)

            self.__gladeBuilder = self.__application.createGladeBuilder('chat')
            self.__gladeBuilder.connect_signals(self)

            self.__window = self.__getGladeObject('windowChat')
            self.__window.get_style_context().add_provider(self.__styleProvider, 800)
            self.__windowTitleTemplate = self.__window.get_title()
            self.__window.show_all()

            self.__reload()

        else:
            self.__window.present()

    def onWindowDestroyed(self, event, userData=None):
        self.__isWindowOpen = False

    def onTypingEvent(self, data=None):
        print("onTypingEvent: " + repr(data))

    def onMessagePostedEvent(self, data=None):
        # Gtk.Window
        window = self.__window

        # Mattermost.ChannelModel
        channelModel = self.__channelModel

        postJson = data['post']
        postData = json.loads(postJson)

        # Mattermost.PostModel
        post = PostModel.fromJsonPostObject(channelModel, postData)

        self.__addPost(post)

        window.present()

        print("onMessagePostedEvent: " + repr(data))

    def onMessageEditedEvent(self, data=None):
        # Mattermost.ChannelModel
        channelModel = self.__channelModel

        # Gtk.TextBuffer
        textbufferChatContent = self.__getGladeObject('textbufferChatContent')

        postJson = data['post']
        postData = json.loads(postJson)

        # Mattermost.PostModel
        post = PostModel.fromJsonPostObject(channelModel, postData)

        # Gtk.TextMark
        beginMark = textbufferChatContent.get_mark("post_%s_message_begin" % post.getId())

        # Gtk.TextMark
        endMark = textbufferChatContent.get_mark("post_%s_message_end" % post.getId())

        textbufferChatContent.delete(
            textbufferChatContent.get_iter_at_mark(beginMark),
            textbufferChatContent.get_iter_at_mark(endMark)
        )

        # Gtk.TextIter
        textIter = textbufferChatContent.get_iter_at_mark(beginMark)

        textbufferChatContent.insert(
            textIter,
            post.getMessage()
        )

        textbufferChatContent.move_mark(endMark, textIter)

        print("onMessageEditedEvent: " + repr(data))

    def onMessageDeletedEvent(self, data=None):
        # ChannelModel
        channelModel = self.__channelModel

        # Gtk.TextBuffer
        textbufferChatContent = self.__getGladeObject('textbufferChatContent')

        postJson = data['post']
        postData = json.loads(postJson)

        # Mattermost.PostModel
        post = PostModel.fromJsonPostObject(channelModel, postData)

        # Gtk.TextMark
        beginMark = textbufferChatContent.get_mark("post_%s_begin" % post.getId())

        # Gtk.TextMark
        endMark = textbufferChatContent.get_mark("post_%s_end" % post.getId())

        textbufferChatContent.delete(
            textbufferChatContent.get_iter_at_mark(beginMark),
            textbufferChatContent.get_iter_at_mark(endMark)
        )

        print("onMessageDeletedEvent: " + repr(data))

    def onSubmitButtonPressed(self, button, data=None):
        self.__doSubmit()

    def onChatInputKeyRelease(self, textInput, event, data=None):
         if event.keyval == 65293: # = enter
            self.__doSubmit()

    def __doSubmit(self):
        # ChannelModel
        channelModel = self.__channelModel

        # Gtk.EntryBuffer
        entrybufferChatInput = self.__getGladeObject('entrybufferChatInput')

        message = entrybufferChatInput.get_text()
        channelModel.createPost(message)
        entrybufferChatInput.set_text("", 0)

    def __reload(self):
        # Gtk.Builder
        gladeBuilder = self.__gladeBuilder

        # Gtk.Window
        window = self.__window

        # ChannelModel
        channelModel = self.__channelModel

        # Gtk.TextView
        textviewChatContent = self.__getGladeObject('textviewChatContent')

        # Gtk.TextBuffer
        textbufferChatContent = self.__getGladeObject('textbufferChatContent')

        self.__styleTextViewAdapter.attachTextView(textviewChatContent)

        # TeamModel
        teamModel = self.__channelModel.getTeamModel()

        # ServerLoggedInModel
        serverModel = teamModel.getServer()

        # UserModel
        selfUser = serverModel.getSelfUser()

        variables = {
            'USERNAME': selfUser.getUseName(),
            'CHANNELNAME': channelModel.getName(),
            'TEAMNAME': teamModel.getName(),
        }

        windowTitle = self.__windowTitleTemplate
        for variableKey in variables:
            windowTitle = windowTitle.replace("%"+variableKey+"%", variables[variableKey])
        window.set_title(windowTitle)

        textbufferChatContent.set_text("", 0)

        posts = channelModel.getPosts()
        for postId in posts:
            # Mattermost.PostModel
            post = posts[postId]

            self.__addPost(post)

    def __addPost(self, post):
        # Mattermost.PostModel

        # TeamModel
        teamModel = self.__channelModel.getTeamModel()

        # ServerLoggedInModel
        serverModel = teamModel.getServer()

        # Gtk.TextBuffer
        textbufferChatContent = self.__getGladeObject('textbufferChatContent')

        # Mattermost.UserModel
        user = post.getUser()

        userId = ""
        userName = ""

        if user != None:
            userId = user.getId()
            userName = user.getUseName()

        # Gtk.TextIter
        textIter = textbufferChatContent.get_end_iter()

        self.__beginPostSection(textIter, "post_%s" % post.getId(), ['post'])

        if self.__lastUserId != userId:


            self.__beginPostSection(textIter, "post_%s_avatar" % post.getId(), ['avatar'])

            if user != None:
                cacheId = "avatar." + user.getId() + ".png"
                avatarImagePath = self.__application.getCacheFilePath(cacheId)

                if not os.path.exists(avatarImagePath):
                    avatarImageData = user.getImage()
                    self.__application.putCache(cacheId, avatarImageData)

                if os.path.exists(avatarImagePath):
                    # GdkPixbuf.Pixbuf
                    pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                        avatarImagePath,
                        width=48,
                        height=48,
                        preserve_aspect_ratio=False
                    )

                    textbufferChatContent.insert_pixbuf(textIter, pixbuf)

            self.__endPostSection(textIter) # end of "post_%s_avatar"


            self.__beginPostSection(textIter, "post_%s_username" % post.getId(), ['username'])

            textbufferChatContent.insert(textIter, userName)

            self.__endPostSection(textIter) # end of "post_%s_username"


            textbufferChatContent.insert(textIter, "\n")

            self.__lastUserId = userId

        self.__beginPostSection(textIter, "post_%s_message" % post.getId(), ['message'])

        message = post.getMessage()

        textbufferChatContent.insert(textIter, message)

        self.__endPostSection(textIter) # end of "post_%s_message"

        if post.hasFiles():
            textbufferChatContent.insert(textIter, "\n")

            for fileId in post.getFileIds():
                cacheId = "file." + fileId + ".dat"
                cachedFilePath = self.__application.getCacheFilePath(cacheId)

                if not os.path.exists(cachedFilePath):
                    # Mattermost.FileModel
                    fileModel = serverModel.getFile(fileId)

                    self.__application.putCache(cacheId, fileModel.getFileContents())

                if os.path.exists(cachedFilePath):
                    isImage = True # TODO: actually find this out
                    if isImage:
                        # GdkPixbuf.Pixbuf
                        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                            cachedFilePath,
                            width=64,
                            height=64,
                            preserve_aspect_ratio=False
                        )


                        self.__beginPostSection(textIter, "post_%s_file_%s" % (post.getId(), fileId), ['file'])

                        textbufferChatContent.insert(textIter, " ")


                        self.__beginPostSection(textIter, "post_%s_file_%s_pixbuf" % (post.getId(), fileId), ['pixbuf'])

                        textbufferChatContent.insert_pixbuf(textIter, pixbuf)

                        self.__endPostSection(textIter) # end of "post_%s_file_%s_pixbuf"


                        self.__endPostSection(textIter) # end of "post_%s_file_%s"

        textbufferChatContent.insert(textIter, "\n")

        self.__endPostSection(textIter) # end of "post_%s"

    def __beginPostSection(self, textIter, name, classes=None):

        # Gtk.TextBuffer
        textbufferChatContent = self.__getGladeObject('textbufferChatContent')

        beginMark = textbufferChatContent.create_mark(
            str(name) + "_begin",
            textIter.copy(),
            True
        )

        # GtkTagTable
        tagTable = textbufferChatContent.get_tag_table()

        self.__sections.append((name, beginMark, classes, tagTable.get_size()))

    def __endPostSection(self, textIter):

        # Gtk.TextBuffer
        textbufferChatContent = self.__getGladeObject('textbufferChatContent')

        name, beginMark, classes, priority = self.__sections.pop()

        # Gtk.TextIter
        beginIter = textbufferChatContent.get_iter_at_mark(beginMark)

        endMark = textbufferChatContent.create_mark(
            str(name) + "_end",
            textIter.copy(),
            True
        )

        tagName = name
        if classes != None and len(classes) > 0:
            tagName += "_" + "_".join(classes)

        # Gtk.TextTag
        textTag = textbufferChatContent.create_tag(tagName)
        textTag.set_priority(priority)

        textbufferChatContent.apply_tag(textTag, beginIter, textIter)
