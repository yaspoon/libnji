from ctypes import *
from jni import *
import Class
from jni import *

class Constructor(object):
    _isInit = False
    _getParameterTypes = None
    _getParameterCount = None
    _getName = None
    _Class = None

    def __init__(self, obj):
        self.obj = obj 
        if(not Constructor._isInit):
            Constructor._Class = Class.fromFullyQualifiedName("Ljava/lang/reflect/Constructor;")
            if(not Constructor._Class):
                print("Failed to find Constructor class")
            Constructor._getParameterCount = GetMethodID(Constructor._Class.getClass(), "getParameterCount", "()I")
            if(not Constructor._getParameterCount):
                print("Failed to find getParameterCount")
            Constructor._getParameterTypes = GetMethodID(Constructor._Class.getClass(), "getParameterTypes", "()[Ljava/lang/Class;")
            if(not Constructor._getParameterTypes):
                print("Failed to find getParameterTypes")
            Constructor._getName = GetMethodID(Constructor._Class.getClass(), "getName", "()Ljava/lang/String;")
            if(not Constructor._getName):
                print("Failed to find getName")
            Constructor._isInit = True
            self.parameter_types = None

    def getParameterTypes(self): 
        self.parameter_types = []
        if(not self.parameter_types):
            param_types = CallObjectMethod(self.obj, Constructor._getParameterTypes)
            length = GetArrayLength(param_types)
            for i in range(length):
                param_type = GetObjectArrayElement(param_types, i)
                self.parameter_types.append(Class.fromJclass(param_type))
        return self.parameter_types

    def getParameterCount(self): 
        return CallObjectMethod(self.obj, Constructor._getParameterCount)

    def getName(self):
        return CallObjectMethod(self.obj, Constructor._getName)
