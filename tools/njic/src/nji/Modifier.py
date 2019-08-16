from .jenv import *
from . import ClassUtils

class Modifier(object):
    _isInit = False
    _Modifier = None
    _isStatic = None
    _getModifiers = None
    _Member = None
    _count = 0

    def __init__(self):
        Modifier._count = Modifier._count + 1
        if(not Modifier._isInit):
            Modifier._Modifier = ClassUtils.fromFullyQualifiedName("Ljava/lang/reflect/Modifier;")
            if(not Modifier._Modifier):
                print("Failed to find Modifier class")
            Modifier._isStatic = GetStaticMethodID(Modifier._Modifier.getClass(), "isStatic", "(I)Z")
            if(not Modifier._isStatic):
                print("Failed to find isStatic")
            Modifier._Member = ClassUtils.fromFullyQualifiedName("Ljava/lang/reflect/Member;")
            if(not Modifier._Member):
                print("Failed to find Member class")
            Modifier._getModifiers = GetMethodID(Modifier._Member.getClass(), "getModifiers", "()I")
            if(not Modifier._getModifiers):
                print("Failed to find getModifiers")
            Modifier._isInit = True

    def __del__(self):
        if(Modifier._isInit and Modifier._count == 1):
            del(Modifier._Modifier)
            Modifier._Modifier = None
            del(Modifier._Member)
            Modifier._Member = None
            Modifier._isInit = False
        Modifier._count = Modifier._count - 1

    def isStatic(self):
        modifiers = self.getModifiers()
        return CallStaticBooleanMethod(Modifier._Modifier.getClass(), Modifier._isStatic, modifiers)

    def getModifiers(self):
        return CallIntMethod(self.obj, Modifier._getModifiers)
