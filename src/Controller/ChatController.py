
from gi.repository import GLib, Gtk, GdkPixbuf, Notify

from ..Model.Mattermost.PostModel import PostModel

import json
import os

class ChatController:
    __gladeBuilder = None        # Gtk.Builder
    __application = None         # Application
    __window = None              # Gtk.Window
    __windowTitleTemplate = None # string
    __channelModel = None        # Mattermost.ChannelModel
    __isWindowOpen = False       # boolean
#    __postTreeIterMap = {}       # dict(Gtk.TreeIter)

    def __init__(self, application, channelModel):
        self.__application = application
        self.__channelModel = channelModel

        channelModel.registerTypingListener(self.onTypingEvent)
        channelModel.registerPostedListener(self.onMessagePostedEvent)
        channelModel.registerPostEditedListener(self.onMessageEditedEvent)
        channelModel.registerPostDeletedListener(self.onMessageDeletedEvent)

    def show(self):
        if not self.__isWindowOpen:
            self.__isWindowOpen = True
            self.__gladeBuilder = self.__application.createGladeBuilder('chat')
            self.__gladeBuilder.connect_signals(self)
            self.__window = self.__gladeBuilder.get_object('windowChat')
            self.__windowTitleTemplate = self.__window.get_title()
            self.__window.show_all()
            self.__reload()

        else:
            self.__window.present()

    def onWindowDestroyed(self, event, userData=None):
        self.__isWindowOpen = False

    def onTypingEvent(self, data=None):
        # Gtk.Builder
        gladeBuilder = self.__gladeBuilder

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
        # Gtk.Builder
        gladeBuilder = self.__gladeBuilder

        # Mattermost.ChannelModel
        channelModel = self.__channelModel

        # Gtk.TextBuffer
        textbufferChatContent = gladeBuilder.get_object('textbufferChatContent')

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
        # Gtk.Builder
        gladeBuilder = self.__gladeBuilder

        # ChannelModel
        channelModel = self.__channelModel

        # Gtk.TextBuffer
        textbufferChatContent = gladeBuilder.get_object('textbufferChatContent')

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
        # Gtk.Builder
        gladeBuilder = self.__gladeBuilder

        # ChannelModel
        channelModel = self.__channelModel

        # Gtk.EntryBuffer
        entrybufferChatInput = gladeBuilder.get_object('entrybufferChatInput')

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

        # Gtk.TextBuffer
        textbufferChatContent = gladeBuilder.get_object('textbufferChatContent')

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

        posts = channelModel.getLastPosts()
        for postId in posts:
            # Mattermost.PostModel
            post = posts[postId]

            self.__addPost(post)

    def __addPost(self, post):
        # Mattermost.PostModel

        # Gtk.Builder
        gladeBuilder = self.__gladeBuilder

        # TeamModel
        teamModel = self.__channelModel.getTeamModel()

        # ServerLoggedInModel
        serverModel = teamModel.getServer()

        # Gtk.TextBuffer
        textbufferChatContent = gladeBuilder.get_object('textbufferChatContent')

        user = post.getUser()

        userId = ""
        userName = ""

        if user != None:
            userId = user.getId()
            userName = user.getUseName()

        # Gtk.TextIter
        textIter = textbufferChatContent.get_end_iter()

        textbufferChatContent.create_mark(
            "post_%s_begin" % post.getId(),
            textIter.copy(),
            True
        )

        textbufferChatContent.insert(textIter, "%s: " % userName, len(userName) + 2)

        textbufferChatContent.create_mark(
            "post_%s_message_begin" % post.getId(),
            textIter.copy(),
            True
        )

        textbufferChatContent.insert(textIter, post.getMessage())

        textbufferChatContent.create_mark(
            "post_%s_message_end" % post.getId(),
            textIter.copy(),
            True
        )

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
                    pixbuf = GdkPixbuf.Pixbuf.new_from_file(
                        cachedFilePath
                    )

                    textbufferChatContent.create_mark(
                        "post_%s_file_%s_begin" % (post.getId(), fileId),
                        textIter.copy(),
                        True
                    )

                    textbufferChatContent.insert(textIter, "\n", 1)

                    textbufferChatContent.create_mark(
                        "post_%s_file_%s_pixbuf_begin" % (post.getId(), fileId),
                        textIter.copy(),
                        True
                    )

                    textbufferChatContent.insert_pixbuf(textIter, pixbuf)

                    textbufferChatContent.create_mark(
                        "post_%s_file_%s_end" % (post.getId(), fileId),
                        textIter.copy(),
                        True
                    )

        textbufferChatContent.insert(textIter, "\n", 1)

        textbufferChatContent.create_mark(
            "post_%s_end" % post.getId(),
            textIter.copy(),
            True
        )
