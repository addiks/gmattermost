
import os

class CacheModel:
    __basePath = None

    def __init__(self, basePath):
        while len(basePath)>0 and basePath[-1] == '/':
            basePath = basePath[0:-1]
        if not os.path.isdir(basePath):
            os.mkdir(basePath)
        self.__basePath = basePath

    def getCacheFilePath(self, cacheId):
        basePath = self.__basePath
        return basePath + "/" + cacheId + ".cache"

    def get(self, cacheId):
        content = None
        filePath = self.getCacheFilePath(cacheId)
        if os.path.exists(filePath):
            with open(filePath, "rb") as fileHandle:
                content = fileHandle.read()
        return content

    def put(self, cacheId, content):
        filePath = self.getCacheFilePath(cacheId)
        with open(filePath, "wb") as fileHandle:
            fileHandle.write(content)
