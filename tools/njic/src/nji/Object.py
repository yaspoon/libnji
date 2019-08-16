from ctypes import *
from .jenv import *

class Object(object):
    _isInit = False
    _Class = None
    _getClass = None
    _count = 0 #Crappy reference counting
    def __init__(self, obj):
        Object._count = Object._count + 1
        self.obj = obj
        if(not Object._isInit):
            Object._Class = FindClass("Ljava/lang/Object;")
            if(not Object._Class):
                print("Failed to find Object class")
            Object._getClass = GetMethodID(Object._Class, "getClass", "()Ljava/lang/Class;")
            if(not Object._getClass):
                print("Failed to find getClass")
            Object._isInit = True

    def __del__(self):
        if(self.obj != None):
            DeleteLocalRef(self.obj)
        if(Object._isInit and Object._count == 1): #Last object clean up static java variables
            print("Destroying Object class")
            DeleteLocalRef(Object._Class)
            Object._Class = None
            Object._isInit = False
        Object._count = Object._count - 1

    def getClass(self):
        return CallObjectMethod(self.obj, Object._getClass)
