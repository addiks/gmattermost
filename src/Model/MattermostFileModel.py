

class MattermostFileModel:
    __fileId = None
    __serverModel = None

    def __init__(self, serverModel, fileSomething):
        pass

    def getFileThumbnail(self):
        raise Exception("*UNIMPLEMENTED*")
        headers, result = self.callServer("GET", "/get_thumbnail")

    def getFilePreview(self):
        raise Exception("*UNIMPLEMENTED*")
        headers, result = self.callServer("GET", "/get_preview")

    def getFileInfo(self):
        raise Exception("*UNIMPLEMENTED*")
        headers, result = self.callServer("GET", "/get_info")

    def getFilePublicLink(self):
        raise Exception("*UNIMPLEMENTED*")
        headers, result = self.callServer("GET", "/get_public_link")

    def callServer(self, method, route, data=None):
        return self.__serverModel.callServer(method, "/files/%s%s" % (self.__fileId, route), data)
