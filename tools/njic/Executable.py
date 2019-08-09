from ctypes import *
from jni import *
import Class
import Object

class Executable(Object.Object):
    _isInit = False
    _getParameterTypes = None
    _getParameterCount = None
    _getDeclaringClass = None
    _getName = None
    _Class = None

    def __init__(self, obj):
        Object.Object.__init__(self, obj)
        if(not Executable._isInit):
            Executable._Class = Class.fromFullyQualifiedName("Ljava/lang/reflect/Executable;")
            if(not Executable._Class):
                print("Failed to find Executable class")
            Executable._getParameterCount = GetMethodID(Executable._Class.getClass(), "getParameterCount", "()I")
            if(not Executable._getParameterCount):
                print("Failed to find getParameterCount")
            Executable._getParameterTypes = GetMethodID(Executable._Class.getClass(), "getParameterTypes", "()[Ljava/lang/Class;")
            if(not Executable._getParameterTypes):
                print("Failed to find getParameterTypes")
            Executable._getDeclaringClass = GetMethodID(Executable._Class.getClass(), "getDeclaringClass", "()Ljava/lang/Class;")
            if(not Executable._getDeclaringClass):
                print("Failed to find getDeclaringClass")
            Executable._isInit = True

    def getDeclaringClass(self):
        return Class.fromJclass(CallObjectMethod(self.obj, Executable._getDeclaringClass))

    def getParameterTypes(self): 
        self.parameter_types = []
        if(not self.parameter_types):
            param_types = CallObjectMethod(self.obj, Executable._getParameterTypes)
            length = GetArrayLength(param_types)
            for i in range(length):
                param_type = GetObjectArrayElement(param_types, i)
                self.parameter_types.append(Class.fromJclass(param_type))
        return self.parameter_types

    def getParameterCount(self): 
        return CallObjectMethod(self.obj, Executable._getParameterCount)

    def descriptor(self):
        fqn = "("
        types = self.getParameterTypes()
        for t in types:
            fqn = fqn + t.internalTypeSignature()
        fqn = fqn + (")")
        return fqn
