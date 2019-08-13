from ctypes import *
from .jenv import *
from . import Class
from . import Object
from . import Executable
from . import Modifier

class Constructor(Executable.Executable, Modifier.Modifier):
    _isInit = False
    _getName = None
    _Class = None

    def __init__(self, obj):
        class_name = "Ljava/lang/reflect/Constructor;"
        Executable.Executable.__init__(self, class_name, obj)
        Modifier.Modifier.__init__(self)
        if(not Constructor._isInit):
            Constructor._Class = Class.fromFullyQualifiedName(class_name)
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
