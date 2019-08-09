from ctypes import *
from jni import *
import Object
import Class
import Executable
import String

class Field(Executable.Executable):
    _isInit = None
    _Class = None
    _getName = None
    _getType = None

    def __init__(self, obj):
        Executable.Executable.__init__(self, obj)
        if(not Field._isInit):
            Field._Class = Class.fromFullyQualifiedName("Ljava/lang/reflect/Field;")
            if(not Field._Class):
                print("Failed to find Field class")
            Field._getName = GetMethodID(Field._Class.getClass(), "getName", "()Ljava/lang/String;")
            if(not Field._getName):
                print("Failed to find getName")
            Field._getType = GetMethodID(Field._Class.getClass(), "getType", "()Ljava/lang/Class;")
            if(not Field._getType):
                print("Failed to find getType")
            Field._isInit = True

    def getName(self):
        return String.String(CallObjectMethod(self.obj, Field._getName))

    def getType(self):
        return Class.fromJclass(CallObjectMethod(self.obj, Field._getType))

    def descriptor(self):
        return self.getType().internalTypeSignature()
