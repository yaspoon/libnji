from ctypes import *
from .jenv import *
from . import ClassUtils
from . import Object
from . import Executable
from . import Modifier

lock = threading.Lock()
tl = threading.local()
class Constructor(Executable.Executable, Modifier.Modifier):
    _isInit = False
    _getName = None
    _Class = None
    _count = 0

    def __init__(self, obj):
        lock.acquire()
        try:
            class_name = "Ljava/lang/reflect/Constructor;"
            Constructor._count = Constructor._count + 1
            Executable.Executable.__init__(self, class_name, obj)
            Modifier.Modifier.__init__(self)
            if(not Constructor._isInit):
                Constructor._Class = ClassUtils.fromFullyQualifiedName(class_name)
                if(not Constructor._Class):
                    print("Failed to find Constructor class")
                Constructor._getName = GetMethodID(Constructor._Class.getClass(), "getName", "()Ljava/lang/String;")
                if(not Constructor._getName):
                    print("Failed to find getName")
                Constructor._isInit = True
                self.parameter_types = None
        finally:
            lock.release()

    def __del__(self):
        lock.acquire()
        try:
            Modifier.Modifier.__del__(self)
            Executable.Executable.__del__(self)
            if(Constructor._isInit and Constructor._count == 1):
                del(Constructor._Class)
                Constructor._Class = None
                Constructor._jenv = None
                Constructor._isInit = False
            Constructor._count = Constructor._count - 1
        finally:
            lock.release()

    def getName(self):
        return CallObjectMethod(self.obj, Constructor._getName)

    def getClass(self):
        return ClassUtils.fromJclass(super(Constructor, self).getClass())

    def descriptor(self):
        desc = super(Constructor, self).descriptor()
        return desc + "V"
