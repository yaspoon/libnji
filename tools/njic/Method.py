from ctypes import *
from jni import *
import Object
import Class
import Executable
import String

class Method(Executable.Executable):
    _isInit = None
    _Class = None
    _getName = None
    _getReturnType = None

    def __init__(self, obj):
        Executable.Executable.__init__(self, obj)
        if(not Method._isInit):
            Method._Class = Class.fromFullyQualifiedName("Ljava/lang/reflect/Method;")
            if(not Method._Class):
                print("Failed to find Method class")
            Method._getName = GetMethodID(Method._Class.getClass(), "getName", "()Ljava/lang/String;")
            if(not Method._getName):
                print("Failed to find getName")
            Method._getReturnType = GetMethodID(Method._Class.getClass(), "getReturnType", "()Ljava/lang/Class;")
            if(not Method._getReturnType):
                print("Failed to find getReturnType")
            Method._isInit = True

    def getName(self):
        return String.String(CallObjectMethod(self.obj, Method._getName))

    def getReturnType(self):
        return Class.fromJclass(CallObjectMethod(self.obj, Method._getReturnType))

    def descriptor(self):
        desc = super(Method, self).descriptor()
        ret_type = self.getReturnType().internalTypeSignature()
        return desc + ret_type

