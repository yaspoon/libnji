from ctypes import *
from .jenv import *

class Object(object):
    _isInit = False
    _Class = None
    _getClass = None
    def __init__(self, obj):
        self.obj = obj
        if(not Object._isInit):
            Object._Class = FindClass("Ljava/lang/Class;")
            if(not Object._Class):
                print("Failed to find Object class")
            Object._getClass = GetMethodID(Object._Class, "getClass", "()Ljava/lang/Class;")
            if(not Object._getClass):
                print("Failed to find getClass")
            Object._isInit = True

    def __del__(self):
        if(self.obj != None):
            DeleteLocalRef(self.obj)

    def getClass(self):
        return CallObjectMethod(self.obj, Object._getClass)


