from ctypes import *
from .jenv import *
from . import Constructor
from . import String
from . import Object
from . import Method
from . import Field
from . import ClassUtils

class Class(object):
    #jmethodIDs
    _isInit = False
    _Class = None
    _getDeclaredConstructors = None
    _getDeclaredMethods = None
    _getDeclaredFields = None
    _getCanonicalName = None
    _getModifiers = None
    _isArray = None
    _getName = None
    _getComponentType = None

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
                #print("Constructors:{}".format(length))
                self.constructors = []
                for i in range(length):
                    constructor = GetObjectArrayElement(constructors, i)
                    self.constructors.append(Constructor.Constructor(constructor))
        return self.constructors

    #Creates python Method objects that wrap the underlying java.lang.reflect.Method
    def getDeclaredMethods(self):
        if(not Class._getDeclaredMethods):
            print("_getDeclaredMethods isn't resolved")
        if(not self.methods):
            methods = CallObjectMethod(self.Class, Class._getDeclaredMethods)
            if(methods):
                length = GetArrayLength(methods)
                #print("methods:{}".format(length))
                self.methods = []
                for i in range(length):
                    method = GetObjectArrayElement(methods, i)
                    self.methods.append(Method.Method(method))
        return self.methods

    #Creates python Field objects that wrap the underlying java.lang.reflect.Field
    def getDeclaredFields(self):
        if(not Class._getDeclaredFields):
            print("_getDeclaredFields isn't resolved")
        if(not self.fields):
            fields = CallObjectMethod(self.Class, Class._getDeclaredFields)
            if(fields):
                length = GetArrayLength(fields)
                #print("fields:{}".format(length))
                self.fields = []
                for i in range(length):
                    field = GetObjectArrayElement(fields, i)
                    self.fields.append(Field.Field(field))
        return self.fields



    def getClass(self):
        return self.Class

    def getCanonicalName(self):
        return _getCanonicalName(self.Class)

    def getName(self):
        return _getName(self.Class)

    def getModifiers(self):
        return _getModifiers(self.Class)

    def isPrimitive(self):
        return _isPrimitive(self.Class)

    def isArray(self):
        return _isArray(self.Class)

    def getComponentType(self):
        return _getComponentType(self.Class)

    @property
    def jname(self):
        name = self.getCanonicalName()
        return str(name).replace(".", "/")

    def internalTypeSignature(self):
        its = str(self.getName()).replace(".", "/")
        if(self.isPrimitive()):
            if(its == "boolean"):
                its = "Z"
            elif(its == "byte"):
                its = "B"
            elif(its == "char"):
                its = "C"
            elif(its == "double"):
                its = "D"
            elif(its == "float"):
                its = "F"
            elif(its == "int"):
                its = "I"
            elif(its == "long"):
                its = "J"
            elif(its == "short"):
                its = "S"
            elif(its == "void"):
                its = "V"
        elif(not self.isArray()):
            its = "L{};".format(its)

        return its 


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
            print("Failed to find isPrimitive")
        Class._isArray = GetMethodID(Class._Class, "isArray", "()Z")
        if(not Class._isArray):
            print("Failed to find isArray")
        Class._getName = GetMethodID(Class._Class, "getName", "()Ljava/lang/String;")
        if(not Class._getName):
            print("Failed to find getName")
        Class._getComponentType = GetMethodID(Class._Class, "getComponentType", "()Ljava/lang/Class;")
        if(not Class._getComponentType):
            print("Failed to find getComponentType")
        Class._getDeclaredMethods = GetMethodID(Class._Class, "getDeclaredMethods", "()[Ljava/lang/reflect/Method;")
        if(not Class._getDeclaredMethods):
            print("Failed to find getDeclaredMethods")
        Class._getDeclaredFields= GetMethodID(Class._Class, "getDeclaredFields", "()[Ljava/lang/reflect/Field;")
        if(not Class._getDeclaredFields):
            print("Failed to find getDeclaredFields")
        Class._isInit = True

def _getCanonicalName(class_obj):
    class_init()
    return String.String(CallObjectMethod(class_obj, Class._getCanonicalName))

def _getModifiers(class_obj):
    class_init()
    return CallIntMethod(class_obj, Class._getModifiers)

def _isPrimitive(class_obj):
    class_init()
    return CallBooleanMethod(class_obj, Class._isPrimitive)

def _isArray(class_obj):
    class_init()
    return CallBooleanMethod(class_obj, Class._isArray)

def _getName(class_obj):
    class_init()
    return String.String(CallObjectMethod(class_obj, Class._getName))

def _getComponentType(class_obj):
    class_init()
    return fromJclass(CallObjectMethod(class_obj, Class._getComponentType))
