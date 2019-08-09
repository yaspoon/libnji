#!/bin/env python2

import pdb
import time
from ctypes import *
from jni import *
from Constructor import *
from Class import *

print("sizeof(JNINativeInterface):" + str(sizeof(JNINativeInterface())))

print("JVM version:{}".format(hex(GetVersion())))

obj = fromFullyQualifiedName("Ljava/lang/String;")
if(obj):
    print("Got Obj")
    print("Constructors:")
    for con in obj.getDeclaredConstructors():
        print(con.descriptor())
    print("Methods:")
    for meth in obj.getDeclaredMethods():
        print(meth.descriptor())
    print("Fields:")
    for field in obj.getDeclaredFields():
        print(str(field.getName()) + " " + field.descriptor())

'''
Object = jni.FindClass("Ljava/lang/Object;")
Object_toString = None
if(Object):
    print("Found Object class")
    Object_toString = jenv.GetMethodID(p_jenv, Object, "toString", "()Ljava/lang/String;")
    if(Object_toString):
        print("Found toString method")

ClassLoader = jenv.FindClass(p_jenv, "Ljava/lang/ClassLoader;")
if(ClassLoader):
    print("Found ClassLoader class")

Constructor = jenv.FindClass(p_jenv, "Ljava/lang/reflect/Constructor;")
Constructor_getParameterTypes = None
if(Constructor):
    print("Found Constructor class")
    Constructor_getParameterTypes = jenv.GetMethodID(p_jenv, Constructor, "getParameterTypes", "()[Ljava/lang/Class;");
    if(Constructor_getParameterTypes):
        print("Found Constructor_getParameterTypes")

Constructor = Constructor(p_jenv, jenv)

ClassLoader_Constructors = Constructor.getDeclaredConstructors()
if(ClassLoader_Constructors):
    print("Found ClassLoader_Constructors")
    ClassLoader_Constructors_len = jenv.GetArrayLength(p_jenv, ClassLoader_Constructors)
    print("Number of ClassLoader_Constructors:{}".format(ClassLoader_Constructors_len))
    for i in range(ClassLoader_Constructors_len):
        constructor = jenv.GetObjectArrayElement(p_jenv, ClassLoader_Constructors, i)
        constructor_string = jenv.CallObjectMethod(p_jenv, constructor, Object_toString)
        if(constructor_string):
            print("Got constructor_string")
            constructor_cstr = jenv.GetStringUTFChars(p_jenv, constructor_string, False)
            print("Constructor:{}".format(constructor_cstr))
        parameter_types = Constructor.getParameterTypes()
        if(parameter_types):
            print("Got parameter_types for constructor")
            parameter_types_len = jenv.GetArrayLength(p_jenv, parameter_types)
            print("parameter_types_len:{}".format(parameter_types_len))

Class = jenv.FindClass(p_jenv, "Ljava/lang/Class;");
if(Class):
    print("Found Class")
    ClassLoader_getConstructors = jenv.GetMethodID(p_jenv, Class, "getDeclaredConstructors", "()[Ljava/lang/reflect/Constructor;");
    if(ClassLoader_getConstructors):
        print("Found ClassLoader_getConstructors")
        ClassLoader_Constructors = jenv.CallObjectMethod(p_jenv, ClassLoader, ClassLoader_getConstructors)
        if(ClassLoader_Constructors):
            print("Found ClassLoader_Constructors")
            ClassLoader_Constructors_len = jenv.GetArrayLength(p_jenv, ClassLoader_Constructors)
            print("Number of ClassLoader_Constructors:{}".format(ClassLoader_Constructors_len))
            for i in range(ClassLoader_Constructors_len):
                constructor = jenv.GetObjectArrayElement(p_jenv, ClassLoader_Constructors, i)
                constructor_string = jenv.CallObjectMethod(p_jenv, constructor, Object_toString)
                if(constructor_string):
                    print("Got constructor_string")
                    constructor_cstr = jenv.GetStringUTFChars(p_jenv, constructor_string, False)
                    print("Constructor:{}".format(constructor_cstr))
                parameter_types = jenv.CallObjectMethod(p_jenv, constructor, Constructor_getParameterTypes)
                if(parameter_types):
                    print("Got parameter_types for constructor")
                    parameter_types_len = jenv.GetArrayLength(p_jenv, parameter_types)
                    print("parameter_types_len:{}".format(parameter_types_len))
'''
