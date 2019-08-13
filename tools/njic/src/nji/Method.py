from ctypes import *
from .jenv import *
from . import Object
from . import Class
from . import Executable
from . import String
from . import Modifier

class Method(Executable.Executable, Modifier.Modifier):
    _isInit = None
    _Class = None
    _getName = None
    _getReturnType = None

    def __init__(self, obj):
        class_name = "Ljava/lang/reflect/Method;"
        Executable.Executable.__init__(self, class_name, obj)
        Modifier.Modifier.__init__(self)
        if(not Method._isInit):
            Method._Class = Class.fromFullyQualifiedName(class_name)
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
