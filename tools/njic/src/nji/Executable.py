from ctypes import *
from .jenv import *
from . import Class
from . import Object

class Executable(Object.Object):
    _isInit = False

    #java-7 doesn't have the Executable class so this is retroactively porting it for that JVM after implementing it originally on java-8
    def __init__(self, class_name, obj):
        super(Executable, self).__init__(obj)
        self._Class = Class.fromFullyQualifiedName(class_name)
        if(not self._Class):
            print("Failed to find class")
        self._getParameterTypes = GetMethodID(self._Class.getClass(), "getParameterTypes", "()[Ljava/lang/Class;")
        if(not self._getParameterTypes):
            print("Failed to find getParameterTypes")
        self._getDeclaringClass = GetMethodID(self._Class.getClass(), "getDeclaringClass", "()Ljava/lang/Class;")
        if(not self._getDeclaringClass):
            print("Failed to find getDeclaringClass")
        if(not Executable._isInit):
            Executable._isInit = True

    def getDeclaringClass(self):
        #return Class.fromJclass(CallObjectMethod(self.obj, Executable._getDeclaringClass))
        return Class.fromJclass(CallObjectMethod(self.obj, self._getDeclaringClass))

    def getParameterTypes(self): 
        self.parameter_types = []
        if(not self.parameter_types):
            param_types = CallObjectMethod(self.obj, self._getParameterTypes)
            length = GetArrayLength(param_types)
            for i in range(length):
                param_type = GetObjectArrayElement(param_types, i)
                self.parameter_types.append(Class.fromJclass(param_type))
        return self.parameter_types

    def descriptor(self):
        fqn = "("
        types = self.getParameterTypes()
        for t in types:
            fqn = fqn + t.internalTypeSignature()
        fqn = fqn + (")")
        return fqn
