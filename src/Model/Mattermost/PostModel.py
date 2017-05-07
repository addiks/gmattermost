
class PostModel:
    __channelModel = None  # ChannelModel
    __id = None            # string
    __createAt = None      # integer
    __updateAt = None      # integer
    __editAt = None        # integer
    __deleteAt = None      # integer
    __isPinned = False     # boolean
    __userId = None        # string
    __channelId = None     # string
    __rootId = None        # string
    __parentId = None      # string
    __originalId = None    # string
    __message = None       # string
    __postType = None      # string
    __props = None         # object
    __hashtags = None      # string
    __pendingPostId = None # string

    @staticmethod
    def fromJsonPostObject(channelModel, data):

        if data['channel_id'] != channelModel.getId():
            pass # TODO: raise Exception

        return PostModel(
            channelModel,
            data['id'],
            data['create_at'],
            data['update_at'],
            data['edit_at'],
            data['delete_at'],
            data['is_pinned'],
            data['user_id'],
            data['channel_id'],
            data['root_id'],
            data['parent_id'],
            data['original_id'],
            data['message'],
            data['type'],
            data['props'],
            data['hashtags'],
            data['pending_post_id'],
        )

    def __init__(
        self,
        channelModel,
        postId,
        createAt,
        updateAt,
        editAt,
        deleteAt,
        isPinned,
        userId,
        channelId,
        rootId,
        parentId,
        originalId,
        message,
        postType,
        props,
        hashtags,
        pendingPostId
    ):
        self.__channelModel = channelModel
        self.__postId = postId
        self.__createAt = createAt
        self.__updateAt = updateAt
        self.__editAt = editAt
        self.__deleteAt = deleteAt
        self.__isPinned = isPinned
        self.__userId = userId
        self.__channelId = channelId
        self.__rootId = rootId
        self.__parentId = parentId
        self.__originalId = originalId
        self.__message = message
        self.__postType = postType
        self.__props = props
        self.__hashtags = hashtags
        self.__pendingPostId = pendingPostId

    def getMessage(self):
        return self.__message

    def getUser(self):
        # TeamModel
        teamModel = self.__channelModel.getTeamModel()

        # ServerLoggedInModel
        serverModel = teamModel.getServer()

        return serverModel.getUserById(self.__userId)
