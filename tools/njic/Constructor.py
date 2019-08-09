from ctypes import *
from jni import *
import Class
import Object
import Executable

class Constructor(Executable.Executable):
    _isInit = False
    _getName = None
    _Class = None

    def __init__(self, obj):
        Executable.Executable.__init__(self, obj)
        if(not Constructor._isInit):
            Constructor._Class = Class.fromFullyQualifiedName("Ljava/lang/reflect/Constructor;")
            if(not Constructor._Class):
                print("Failed to find Constructor class")
            Constructor._getName = GetMethodID(Constructor._Class.getClass(), "getName", "()Ljava/lang/String;")
            if(not Constructor._getName):
                print("Failed to find getName")
            Constructor._isInit = True
            self.parameter_types = None

    def getName(self):
        return CallObjectMethod(self.obj, Constructor._getName)

    def getClass(self):
        return Class.fromJclass(super(Constructor, self).getClass())

    def descriptor(self):
        desc = super(Constructor, self).descriptor()
        return desc + "V"
