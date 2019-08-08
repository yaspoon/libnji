from ctypes import *
from jni import *
import Constructor

class Class(object):
    #jmethodIDs
    _isInit = False
    _Class = None
    _getDeclaredConstructors = None
    _getCanonicalName = None
    _getModifiers = None

    def __init__(self):
        class_init()
        self.fqname = None
        self.Class = None
        self.constructors = None
        self.methods = None
        self.fields = None

    def __str__(self):
        pass

    #Creates python Constructor objects that wrap the underlying java.lang.reflect.Constructor
    def getDeclaredConstructors(self):
        if(not Class._getDeclaredConstructors):
            print("_getDeclaredConstructors isn't resolved")
        if(not self.constructors):
            constructors = CallObjectMethod(self.Class, Class._getDeclaredConstructors)
            if(constructors):
                length = GetArrayLength(constructors)
                print("Constructors:{}".format(length))
                self.constructors = []
                for i in range(length):
                    constructor = GetObjectArrayElement(constructors, i)
                    self.constructors.append(Constructor.Constructor(constructor))
        return self.constructors

    def getClass(self):
        return self.Class

    def getCanonicalName(self):
        return _getCanonicalName(self.Class)

def class_init():
    if(not Class._isInit):
        Class._Class = FindClass("Ljava/lang/Class;")
        if(not Class._Class):
            print("Failed to find java/lang/Class")
        Class._getDeclaredConstructors = GetMethodID(Class._Class, "getDeclaredConstructors", "()[Ljava/lang/reflect/Constructor;")
        if(not Class._getDeclaredConstructors):
            print("Failed to find getDeclaredConstructors")
        Class._getCanonicalName = GetMethodID(Class._Class, "getCanonicalName", "()Ljava/lang/String;")
        if(not Class._getCanonicalName):
            print("Failed to find getCanonicalName")
        Class._getModifiers = GetMethodID(Class._Class, "getModifiers", "()I")
        if(not Class._getModifiers):
            print("Failed to find getModifiers")
        Class._isPrimitive = GetMethodID(Class._Class, "isPrimitive", "()Z")
        if(not Class._isPrimitive):
            print("Failed to find _isPrimitive")
        Class._isInit = True

def _getCanonicalName(class_obj):
    class_init()
    return CallObjectMethod(class_obj, Class._getCanonicalName)

def _getModifiers(class_obj):
    class_init()
    return CallIntMethod(class_obj, Class._getModifiers)

def _isPrimitive(class_obj):
    class_init()
    return CallBooleanMethod(class_obj, Class._isPrimitive)

def fromFullyQualifiedName(fqname):
    class_init()
    self = Class()
    self.fqname = fqname
    self.Class = FindClass(self.fqname)
    if(not self.Class):
        print("Failed to find class:{}".format(fqname))
    self.constructors = None
    self.methods = None
    self.fields = None
    return self

def fromJclass(class_obj):
    class_init()
    self = Class()
    fqname_jstr = _getCanonicalName(class_obj)
    fqname = GetStringUTFChars(fqname_jstr, False)
    if(not _isPrimitive):
        fqname = "L{};".format(fqname)
        fqname = fqname.replace('.', '/')

    self.fqname = fqname
    self.Class = class_obj

    return self

