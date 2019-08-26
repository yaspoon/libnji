from ctypes import *
from .jenv import *
from . import Object
from . import ClassUtils
from . import String
from . import Modifier
import threading

lock = threading.Lock()
tl = threading.local()
class Field(Object.Object, Modifier.Modifier):
    _isInit = None
    _Class = None
    _getName = None
    _getType = None
    _count = 0
    _Jni = None

    def __init__(self, obj):
        lock.acquire()
        try:
            Field._count = Field._count + 1
            class_name = "Ljava/lang/reflect/Field;"
            Object.Object.__init__(self, obj)
            Modifier.Modifier.__init__(self)
            if(not Field._isInit):
                Field._Jni = getJni()
                Field._Class = ClassUtils.fromFullyQualifiedName(class_name)
                if(not Field._Class):
                    print("Failed to find Field class")
                Field._getName = GetMethodID(Field._Class.getClass(), "getName", "()Ljava/lang/String;")
                if(not Field._getName):
                    print("Failed to find getName")
                Field._getType = GetMethodID(Field._Class.getClass(), "getType", "()Ljava/lang/Class;")
                if(not Field._getType):
                    print("Failed to find getType")
                Field._isInit = True
        finally:
            lock.release()

    def __del__(self):
        lock.acquire()
        try:
            Modifier.Modifier.__del__(self)
            if(Field._isInit and Field._count == 1):
                del(Field._Class)
                Field._Class = None
                Field._isInit = False
            Field._count = Field._count - 1
        finally:
            lock.release()

    def getName(self):
        return String.String(CallObjectMethod(self.obj, Field._getName))

    def getType(self):
        return ClassUtils.fromJclass(CallObjectMethod(self.obj, Field._getType))

    def descriptor(self):
        return self.getType().internalTypeSignature()
