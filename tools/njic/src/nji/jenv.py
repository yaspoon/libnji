from ctypes import *

import os

#__all__ = ['JavaVMOption', 'JavaVMInitArgs', 'jobject', 'jclass', 'jthrowable', "jstring", "jarray", "jobjectArray", "jmethodID", "jfieldID", "jvalue", "JNINativeInterface", "JNIEnv", "Jni"]

JNI_OK = c_int(0)
'''
typedef struct JavaVMOption {
    char *optionString;  /* the option as a string in the default platform encoding */
    void *extraInfo;
} JavaVMOption;
'''
class JavaVMOption(Structure):
    _fields_ = [("optionString", c_char_p),
                ("extraInfo", c_void_p)]

'''
struct JNIInvokeInterface_ {
    void *reserved0;
    void *reserved1;
    void *reserved2;

    jint (JNICALL *DestroyJavaVM)(JavaVM *vm);

    jint (JNICALL *AttachCurrentThread)(JavaVM *vm, void **penv, void *args);

    jint (JNICALL *DetachCurrentThread)(JavaVM *vm);

    jint (JNICALL *GetEnv)(JavaVM *vm, void **penv, jint version);

    jint (JNICALL *AttachCurrentThreadAsDaemon)(JavaVM *vm, void **penv, void *args);
};
'''

class  JNIInvokeInterface(Structure):
    pass

JavaVM = POINTER(JNIInvokeInterface)

JNIInvokeInterface._fields_ = [
            ("reserved0", c_void_p),
            ("reserved1", c_void_p),
            ("reserved2", c_void_p),
            ("DestroyJavaVM", CFUNCTYPE(c_int, POINTER(JavaVM))),
            ("AttachCurrentThread", CFUNCTYPE(c_int, POINTER(JavaVM), POINTER(c_void_p), c_void_p)),
            ("DetachCurrentThread", CFUNCTYPE(c_int, POINTER(JavaVM))),
            ("GetEnv", CFUNCTYPE(c_int, POINTER(JavaVM), POINTER(c_void_p), c_int)),
            ("AttachCurrentThreadAsDaemon", CFUNCTYPE(POINTER(JavaVM), POINTER(c_void_p), c_void_p))
           ]

'''
typedef struct JavaVMInitArgs {
    jint version;

    jint nOptions;
    JavaVMOption *options;
    jboolean ignoreUnrecognized;
} JavaVMInitArgs;
'''

class JavaVMInitArgs(Structure):
    _fields_ = [("version", c_int),
                ("nOptions", c_int),
                ("options", POINTER(JavaVMOption)),
                ("ignoreUnrecognized", c_bool)]

#Incomplete types aka forward declared
jobject = c_void_p
jclass = jobject
jthrowable = jobject
jstring = jobject
jarray = jobject
jobjectArray = jarray

jmethodID = c_void_p
jfieldID = c_void_p


class jvalue(Union):
    _fields_ = [
                ("z", c_bool),
                ("b", c_byte),
                ("c", c_char),
                ("s", c_short),
                ("i", c_int),
                ("j", c_long),
                ("f", c_float),
                ("d", c_double),
                ("l", jobject)
            ]

#Because functions inside JNINativeInterface take JNINativeInterface pointers we need to "predeclare" the JNINativeInterface to make python happy
class JNINativeInterface(Structure):
    pass

JNIEnv = POINTER(JNINativeInterface)

JNINativeInterface._fields_ = [
            ("reserved0", c_void_p), #0
            ("reserved1", c_void_p), #1
            ("reserved2", c_void_p), #2
            ("reserved3", c_void_p), #3
            ("GetVersion", CFUNCTYPE(c_int, POINTER(JNIEnv))), #4

            ("DefineClass", CFUNCTYPE(jclass, POINTER(JNIEnv), c_char_p, jobject, c_char_p, c_size_t)), #5
            ("FindClass", CFUNCTYPE(jclass, POINTER(JNIEnv), c_char_p)), #6

            ("FromReflectedMethod", CFUNCTYPE(jmethodID, POINTER(JNIEnv), jobject)), #7
            ("FromReflectedField", CFUNCTYPE(jfieldID, POINTER(JNIEnv), jobject)), #8
            ("ToReflectedMethod", CFUNCTYPE(jobject, POINTER(JNIEnv), jclass, jmethodID, c_bool)), #9

            ("GetSuperClass", CFUNCTYPE(jclass, POINTER(JNIEnv), jclass)), #10
            ("IsAssignableFrom", CFUNCTYPE(c_bool, POINTER(JNIEnv), jclass, jclass)), #11

            ("ToReflectedField", CFUNCTYPE(jobject, POINTER(JNIEnv), jclass, jfieldID, c_bool)), #12


            ("Throw", CFUNCTYPE(c_int, POINTER(JNIEnv), jobject)), #13
            ("ThrowNew", CFUNCTYPE(c_int, POINTER(JNIEnv), jclass, c_char_p)), #14

            ("ExceptionOccurred", CFUNCTYPE(jthrowable, POINTER(JNIEnv))), #15
            ("ExceptionDescribe", CFUNCTYPE(None, POINTER(JNIEnv))), #16
            ("ExceptionClear", CFUNCTYPE(None, POINTER(JNIEnv))), #17
            ("FatalError", CFUNCTYPE(None, POINTER(JNIEnv), c_char_p)), #18

            ("PushLocalFrame", CFUNCTYPE(c_int, POINTER(JNIEnv), c_int)), #19
            ("PopLocalFrame", CFUNCTYPE(jobject, POINTER(JNIEnv), jobject)), #20

            ("NewGlobalRef", CFUNCTYPE(jobject, POINTER(JNIEnv), jobject)), #21
            ("DeleteGlobalRef", CFUNCTYPE(None, POINTER(JNIEnv), jobject)), #22
            ("DeleteLocalRef", CFUNCTYPE(None, POINTER(JNIEnv), jobject)), #23

            ("IsSameObject", CFUNCTYPE(c_bool, POINTER(JNIEnv), jobject, jobject)), #24
            ("NewLocalRef", CFUNCTYPE(jobject, POINTER(JNIEnv), jobject)), #25

            ("EnsureLocalCapacity", CFUNCTYPE(c_int, POINTER(JNIEnv), c_int)), #26

            ("AllocObject", CFUNCTYPE(jobject, POINTER(JNIEnv), jclass)), #27
            ("NewObject", CFUNCTYPE(jobject, POINTER(JNIEnv), jclass, jmethodID)), #28 #This is a vararg method but I have no idea how to do that....
            ("NewObjectV", CFUNCTYPE(jobject, POINTER(JNIEnv), jclass, jmethodID, c_void_p)), #29
            ("NewObjectA", CFUNCTYPE(jobject, POINTER(JNIEnv), jclass, jmethodID, POINTER(jvalue))), #30

            ("GetObjectClass", CFUNCTYPE(jclass, POINTER(JNIEnv), jobject)), #31

            ("IsInstanceOf", CFUNCTYPE(c_bool, POINTER(JNIEnv), jobject, jclass)), #32

            ("GetMethodID", CFUNCTYPE(jmethodID, POINTER(JNIEnv), jclass, c_char_p, c_char_p)), #33

            ("CallObjectMethod", CFUNCTYPE(jobject, POINTER(JNIEnv), jobject, jmethodID)), #34
            ("CallObjectMethodV", CFUNCTYPE(jobject, POINTER(JNIEnv), jobject, jmethodID, c_void_p)), #35
            ("CallObjectMethodA", CFUNCTYPE(jobject, POINTER(JNIEnv), jobject, jmethodID, POINTER(jvalue))), #36

            ("CallBooleanMethod", CFUNCTYPE(c_bool, POINTER(JNIEnv), jobject, jmethodID)), #37
            ("CallBooleanMethodV", c_void_p), #38
            ("CallBooleanMethodA", CFUNCTYPE(c_bool, POINTER(JNIEnv), jobject, jmethodID, POINTER(jvalue))), #39

            ("CallByteMethod", c_void_p), #40
            ("CallByteMethodV", c_void_p), #41
            ("CallByteMethodA", c_void_p), #42

            ("CallCharMethod", c_void_p), #43
            ("CallCharMethodV", c_void_p), #44
            ("CallCharMethodA", c_void_p), #45

            ("CallShortMethod", c_void_p), #46
            ("CallShortMethodV", c_void_p), #47
            ("CallShortMethodA", c_void_p), #48

            ("CallIntMethod", CFUNCTYPE(c_int, POINTER(JNIEnv), jobject, jmethodID)), #49
            ("CallIntMethodV", c_void_p), #50
            ("CallIntMethodA", CFUNCTYPE(c_int, POINTER(JNIEnv), jobject, jmethodID, POINTER(jvalue))), #51

            ("CallLongMethod", c_void_p), #52
            ("CallLongMethodV", c_void_p), #53
            ("CallLongMethodA", c_void_p), #54

            ("CallFloatMethod", c_void_p), #55
            ("CallFloatMethodV", c_void_p), #56
            ("CallFloatMethodA", c_void_p), #57

            ("CallDoubleMethod", c_void_p), #58
            ("CallDoubleMethodV", c_void_p), #59
            ("CallDoubleMethodA", c_void_p), #60

            ("CallVoidMethod", c_void_p), #61
            ("CallVoidMethodV", c_void_p), #62
            ("CallVoidMethodA", c_void_p), #63

            ("CallNonvirtualObjectMethod", c_void_p), #64
            ("CallNonvirtualObjectMethodV", c_void_p), #65
            ("CallNonvirtualObjectMethodA", c_void_p), #66

            ("CallNonvirtualBooleanMethod", c_void_p), #67
            ("CallNonvirtualBooleanMethodV", c_void_p), #68
            ("CallNonvirtualBooleanMethodA", c_void_p), #69

            ("CallNonvirtualByteMethod", c_void_p), #70
            ("CallNonvirtualByteMethodV", c_void_p), #71
            ("CallNonvirtualByteMethodA", c_void_p), #72

            ("CallNonvirtualCharMethod", c_void_p), #73
            ("CallNonvirtualCharMethodV", c_void_p), #74
            ("CallNonvirtualCharMethodA", c_void_p), #75

            ("CallNonvirtualShortMethod", c_void_p), #76
            ("CallNonvirtualShortMethodV", c_void_p), #77
            ("CallNonvirtualShortMethodA", c_void_p), #78

            ("CallNonvirtualIntMethod", c_void_p), #79
            ("CallNonvirtualIntMethodV", c_void_p), #80
            ("CallNonvirtualIntMethodA", c_void_p), #81

            ("CallNonvirtualLongMethod", c_void_p), #82
            ("CallNonvirtualLongMethodV", c_void_p), #83
            ("CallNonvirtualLongMethodA", c_void_p), #84

            ("CallNonvirtualFloatMethod", c_void_p), #85
            ("CallNonvirtualFloatMethodV", c_void_p), #86
            ("CallNonvirtualFloatMethodA", c_void_p), #87

            ("CallNonvirtualDoubleMethod", c_void_p), #88
            ("CallNonvirtualDoubleMethodV", c_void_p), #89
            ("CallNonvirtualDoubleMethodA", c_void_p), #90

            ("CallNonvirtualVoidMethod", c_void_p), #91
            ("CallNonvirtualVoidMethodV", c_void_p), #92
            ("CallNonvirtualVoidMethodA", c_void_p), #93

            ("GetFieldID", c_void_p), #94

            ("GetObjectField", c_void_p), #95
            ("GetBooleanField", c_void_p), #96
            ("GetByteField", c_void_p), #97
            ("GetCharField", c_void_p), #98
            ("GetShortField", c_void_p), #99
            ("GetIntField", c_void_p), #100
            ("GetLongField", c_void_p), #101
            ("GetFloatField", c_void_p), #102
            ("GetDoubleField", c_void_p), #103

            ("SetObjectField", c_void_p), #104
            ("SetBooleanField", c_void_p), #105
            ("SetByteField", c_void_p), #106
            ("SetCharField", c_void_p), #107
            ("SetShortField", c_void_p), #108
            ("SetIntField", c_void_p), #109
            ("SetLongField", c_void_p), #110
            ("SetFloatField", c_void_p), #111
            ("SetDoubleField", c_void_p), #112

            ("GetStaticMethodID", CFUNCTYPE(jmethodID, POINTER(JNIEnv), jclass, c_char_p, c_char_p)), #113

            ("CallStaticObjectMethod", c_void_p), #114
            ("CallStaticObjectMethodV", c_void_p),
            ("CallStaticObjectMethodA", c_void_p),

            ("CallStaticBooleanMethod", CFUNCTYPE(c_bool, POINTER(JNIEnv), jclass, jmethodID)),
            ("CallStaticBooleanMethodV", CFUNCTYPE(c_bool, POINTER(JNIEnv), jclass, jmethodID, c_void_p)),
            ("CallStaticBooleanMethodA", CFUNCTYPE(c_bool, POINTER(JNIEnv), jclass, jmethodID, POINTER(jvalue))),

            ("CallStaticByteMethod", c_void_p),
            ("CallStaticByteMethodV", c_void_p),
            ("CallStaticByteMethodA", c_void_p),

            ("CallStaticCharMethod", c_void_p),
            ("CallStaticCharMethodV", c_void_p),
            ("CallStaticCharMethodA", c_void_p),

            ("CallStaticShortMethod", c_void_p),
            ("CallStaticShortMethodV", c_void_p),
            ("CallStaticShortMethodA", c_void_p),

            ("CallStaticIntMethod", c_void_p),
            ("CallStaticIntMethodV", c_void_p),
            ("CallStaticIntMethodA", c_void_p),

            ("CallStaticLongMethod", c_void_p),
            ("CallStaticLongMethodV", c_void_p),
            ("CallStaticLongMethodA", c_void_p),

            ("CallStaticFloatMethod", c_void_p),
            ("CallStaticFloatMethodV", c_void_p),
            ("CallStaticFloatMethodA", c_void_p),

            ("CallStaticDoubleMethod", c_void_p),
            ("CallStaticDoubleMethodV", c_void_p),
            ("CallStaticDoubleMethodA", c_void_p),

            ("CallStaticVoidMethod", c_void_p),
            ("CallStaticVoidMethodV", c_void_p),
            ("CallStaticVoidMethodA", c_void_p), #143

            ("GetStaticFieldID", c_void_p), #144

            ("GetStaticObjectField", c_void_p), #145
            ("GetStaticBooleanField", c_void_p),
            ("GetStaticByteField", c_void_p),
            ("GetStaticCharField", c_void_p),
            ("GetStaticShortField", c_void_p),
            ("GetStaticIntField", c_void_p),
            ("GetStaticLongField", c_void_p),
            ("GetStaticFloatField", c_void_p),
            ("GetStaticDoubleField", c_void_p), #153

            ("SetStaticObjectField", c_void_p), #154
            ("SetStaticBooleanField", c_void_p),
            ("SetStaticByteField", c_void_p),
            ("SetStaticCharField", c_void_p),
            ("SetStaticShortField", c_void_p),
            ("SetStaticIntField", c_void_p),
            ("SetStaticLongField", c_void_p),
            ("SetStaticFloatField", c_void_p),
            ("SetStaticDoubleField", c_void_p), #162

            ("NewString", CFUNCTYPE(jstring, POINTER(JNIEnv), c_char_p, c_size_t)), #163
            ("GetStringLength", c_void_p), #164
            ("GetStringChars", c_void_p), #165
            ("ReleaseStringChars", c_void_p), #166
            ("NewStringUTF", c_void_p), #167
            ("GetStringUTFLength", CFUNCTYPE(c_size_t, POINTER(JNIEnv), jstring)), #168
            ("GetStringUTFChars", CFUNCTYPE(POINTER(c_char), POINTER(JNIEnv), jstring, c_bool)), #169
            ("ReleaseStringUTFChars", CFUNCTYPE(None, POINTER(JNIEnv), jstring, c_char_p)), #170

            ("GetArrayLength", CFUNCTYPE(c_size_t, POINTER(JNIEnv), jarray)), #171
            ("NewObjectArray", CFUNCTYPE(jobjectArray, POINTER(JNIEnv), c_size_t, jclass, jobject)), #172
            ("GetObjectArrayElement", CFUNCTYPE(jobject, POINTER(JNIEnv), jobjectArray, c_size_t)), #173
            ("SetObjectArrayElement", CFUNCTYPE(None, POINTER(JNIEnv), jobjectArray, c_size_t, jobject)), #174

            ("NewBooleanArray", c_void_p), #175
            ("NewByteArray", c_void_p),
            ("NewCharArray", c_void_p),
            ("NewShortArray", c_void_p),
            ("NewIntArray", c_void_p),
            ("NewLongArray", c_void_p),
            ("NewFloatArray", c_void_p),
            ("NewDoubleArray", c_void_p), #182

            ("GetBooleanArrayElements", c_void_p), #183
            ("GetByteArrayElements", c_void_p),
            ("GetCharArrayElements", c_void_p),
            ("GetShortArrayElements", c_void_p),
            ("GetIntArrayElements", c_void_p),
            ("GetLongArrayElements", c_void_p),
            ("GetFloatArrayElements", c_void_p),
            ("GetDoubleArrayElements", c_void_p), #190

            ("ReleaseBooleanArrayElements", c_void_p), #191
            ("ReleaseByteArrayElements", c_void_p),
            ("ReleaseCharArrayElements", c_void_p),
            ("ReleaseShortArrayElements", c_void_p),
            ("ReleaseIntArrayElements", c_void_p),
            ("ReleaseLongArrayElements", c_void_p),
            ("ReleaseFloatArrayElements", c_void_p),
            ("ReleaseDoubleArrayElements", c_void_p), #198

            ("GetBooleanArrayRegion", c_void_p), #199
            ("GetByteArrayRegion", c_void_p),
            ("GetCharArrayRegion", c_void_p),
            ("GetShortArrayRegion", c_void_p),
            ("GetIntArrayRegion", c_void_p),
            ("GetLongArrayRegion", c_void_p),
            ("GetFloatArrayRegion", c_void_p),
            ("GetDoubleArrayRegion", c_void_p), #206

            ("SetBooleanArrayRegion", c_void_p), #207
            ("SetByteArrayRegion", c_void_p),
            ("SetCharArrayRegion", c_void_p),
            ("SetShortArrayRegion", c_void_p),
            ("SetIntArrayRegion", c_void_p),
            ("SetLongArrayRegion", c_void_p),
            ("SetFloatArrayRegion", c_void_p),
            ("SetDoubleArrayRegion", c_void_p), #214

            ("RegisterNatives", CFUNCTYPE(jobject, POINTER(JNIEnv), jobject, POINTER(jvalue))), #215
            ("UnregisterNatives", c_void_p), #216

            ("MonitorEnter", c_void_p), #217
            ("MonitorExit", c_void_p), #218

            ("GetJavaVM", c_void_p), #219

            ("GetStringRegion", c_void_p), #220
            ("GetStringUTFRegion", c_void_p), #221

            ("GetPrimitiveArrayCritical", c_void_p), #222
            ("ReleasePrimitiveArrayCritical", c_void_p), #223

            ("GetStringCritical", c_void_p), #224
            ("ReleaseStringCritical", c_void_p), #225

            ("NewWeakGlobalRef", c_void_p), #226
            ("DeleteWeakGlobalRef", c_void_p), #227

            ("ExceptionCheck", c_void_p), #228

            ("NewDirectByteBuffer", c_void_p), #229
            ("GetDirectBufferAddress", c_void_p), #230
            ("GetDirectBufferCapacity", c_void_p), #231

            ("GetObjectRefType", c_void_p) #232
        ]

class __Jni:
    def __init__(self):
        self.library_path = None
        self.isInit = False
        self.libjvm = None
        self.p_jenv = None
        self.jenv = None
        self.p_jvm = None
        self.jvm = None
        self.classpath = None

    def __del__(self):
        if(self.isInit):
            ret = self.jvm.DestroyJavaVM(self.p_jvm)
            if(ret != 0):
                raise IOError("Failed to destroy JVM error:{}".format(ret))
            self.isInit = False

Jni = __Jni()

#Do some hacky path finding to try and find where libjvm.so lives
def find_libjvm():
    #if JAVA_HOME is set look underneath that path first
    # java7-9 'jre/lib/ARCH/server/libjvm.so'
    # java10 > 'lib/server/libjvm.so']
    libjvm = None
    suffix_paths = ['lib/server/libjvm.so']
    for arch in ['amd64', 'i386', 'arm64']:
        suffix_paths.append('jre/lib/{}/server/libjvm.so'.format(arch))
    java_home = os.getenv('JAVA_HOME')
    if(java_home):
        for suffix in suffix_paths:
            path = os.path.join(java_home, suffix)
            #print("Checking for libjvm.so at:{}".format(path))
            if(os.path.exists(path) and os.path.isfile(path)):
                #print("Found libjvm.so")
                libjvm = path
                break
    else:
        #Welp lets just take an educated guess. This is based on Arch and ubuntu 18.04 paths
        prefixs = []
        for number in ['7', '8', '9', '10', '11', '12']:
            for name_suffix in ['', '-i386', '-amd64', '-arm64']:
                prefix = '/usr/lib/jvm/java-{}-openjdk{}'.format(number, name_suffix)
                for suffix in suffix_paths:
                    path = os.path.join(prefix, suffix)
                    #print("Checking for libjvm.so at:{}".format(path))
                    if(os.path.exists(path) and os.path.isfile(path)):
                        #print("Found libjvm.so")
                        libjvm = path
                        break
                if(libjvm != None):
                    break
            if(libjvm != None):
                break
    return libjvm

def SetClassPath(classpath):
    built_classpath = ""
    if(isinstance(classpath, list)):
        for path in classpath:
            built_classpath = built_classpath + path
            if(len(classpath) > 1):
                built_classpath = built_classpath + ':'
    elif(isinstance(classpath, str)):
        built_classpath = classpath
    else:
        raise IOError("Unknown classpath type:{}".format(str(type(classpath))))
    Jni.classpath = built_classpath

#Do init
def init():
    if(not Jni.isInit):
        Jni.library_path = find_libjvm()
        if(Jni.library_path is None):
            raise IOError("Failed to find libjvm.so")

        Jni.libjvm = cdll.LoadLibrary(Jni.library_path)

        JNI_CreateJavaVM = getattr(Jni.libjvm, 'JNI_CreateJavaVM')

        JNI_CreateJavaVM.argtypes = [POINTER(POINTER(JavaVM)), POINTER(POINTER(JNIEnv)), POINTER(JavaVMInitArgs)]
        JNI_CreateJavaVM.restype = c_int

        p_jvm = cast(c_void_p(None), POINTER(JavaVM))
        p_jenv = cast(c_void_p(None), POINTER(JNIEnv))

        vm_args = JavaVMInitArgs()
        vm_args.version = 0x00010004
        vm_args.nOptions = 0

        vm_options = None
        if(Jni.classpath):
            vm_args.nOptions = 1
            OneVmOption = JavaVMOption * 1
            vm_options = OneVmOption()
            vm_options[0].optionString = c_char_p('-Djava.class.path={}'.format(Jni.classpath).encode('utf-8'))


        vm_args.options = cast(vm_options, POINTER(JavaVMOption))
        vm_args.ignoreUnrecognized = c_bool(True)

        ret = JNI_CreateJavaVM(pointer(p_jvm), pointer(p_jenv), byref(vm_args))

        Jni.p_jvm = p_jvm #JNIInvokeInterface **
        #Get underlying object aka deref pointer
        jvm = p_jvm.contents #JNIInvokeInterface *
        Jni.jvm = jvm.contents #JNIInvokeInterface

        Jni.p_jenv = p_jenv

        #Get underlying object aka deref pointer
        jenv = Jni.p_jenv.contents # JNINativeInterface *
        Jni.jenv = jenv.contents #JNINativeInterface
        Jni.isInit = True

def GetVersion():
    init()
    ret = Jni.jenv.GetVersion(Jni.p_jenv)
    ExceptionClear()
    return ret

def FindClass(fqname):
    init()
    ret = Jni.jenv.FindClass(Jni.p_jenv, fqname.encode('utf-8'))
    ExceptionClear()
    return ret

def GetMethodID(Class, name, sig):
    init()
    ret = Jni.jenv.GetMethodID(Jni.p_jenv, Class, name.encode('utf-8'), sig.encode('utf-8'))
    ExceptionClear()
    return ret

def CallObjectMethod(obj, method, *args):
    init()
    jvalues = argsToJvalueArray(args)
    meth = Jni.jenv.CallObjectMethodA
    meth.restype = jobject
    if(jvalues == None):
        meth.argtypes = [POINTER(JNIEnv), jobject, jmethodID]
        ret = meth(Jni.p_jenv, obj, method)
        ExceptionClear()
        return ret
    else:
        meth.argtypes = [POINTER(JNIEnv), jobject, jmethodID, POINTER(ARRAY(jvalue, len(args)))]
        ret = meth(Jni.p_jenv, obj, method, pointer(jvalues))
        ExceptionClear()
        return ret

def GetArrayLength(array):
    init()
    ret = Jni.jenv.GetArrayLength(Jni.p_jenv, array)
    ExceptionClear()
    return ret

def GetObjectArrayElement(array, index):
    init()
    ret = Jni.jenv.GetObjectArrayElement(Jni.p_jenv, array, index)
    ExceptionClear()
    return ret

def GetStringUTFChars(string, isCopy):
    init()
    c_str = Jni.jenv.GetStringUTFChars(Jni.p_jenv, string, isCopy)
    ExceptionClear()
    return c_str

def CallIntMethod(obj, method, *args):
    init()
    jvalues = argsToJvalueArray(args)
    meth = Jni.jenv.CallIntMethodA
    meth.restype = c_int 
    if(jvalues == None):
        meth.argtypes = [POINTER(JNIEnv), jobject, jmethodID]
        ret = meth(Jni.p_jenv, obj, method)
        ExceptionClear()
        return ret
    else:
        meth.argtypes = [POINTER(JNIEnv), jobject, jmethodID, POINTER(ARRAY(jvalue, len(args)))]
        ret = meth(Jni.p_jenv, obj, method, pointer(jvalues))
        ExceptionClear()
        return ret

def CallBooleanMethod(obj, method, *args):
    init()
    ret = Jni.jenv.CallBooleanMethod(Jni.p_jenv, obj, method)
    ExceptionClear()
    return ret

def ReleaseStringUTFChars(string, c_str):
    init()
    Jni.jenv.ReleaseStringUTFChars(Jni.p_jenv, string, c_str)
    ExceptionClear()

def GetStaticMethodID(Class, name, sig):
    init()
    ret = Jni.jenv.GetStaticMethodID(Jni.p_jenv, Class, name.encode('utf-8'), sig.encode('utf-8'))
    ExceptionClear()
    return ret

def NewString(c_string, length):
    init()
    ret = Jni.jenv.NewString(Jni.p_jenv, c_string, length)
    ExceptionClear()
    return ret

def DeleteLocalRef(obj):
    init()
    Jni.jenv.DeleteLocalRef(Jni.p_jenv, obj)
    ExceptionClear()

def CallStaticBooleanMethod(Class, method, *args):
    init()
    jvalues = argsToJvalueArray(args)
    meth = Jni.jenv.CallStaticBooleanMethodA 
    meth.restype = c_bool 
    if(jvalues == None):
        meth.argtypes = [POINTER(JNIEnv), jclass, jmethodID]
        ret = meth(Jni.p_jenv, Class, method)
        ExceptionClear()
        return ret
    else:
        meth.argtypes = [POINTER(JNIEnv), jclass, jmethodID, POINTER(ARRAY(jvalue, len(args)))]
        ret = meth(Jni.p_jenv, Class, method, pointer(jvalues))
        ExceptionClear()
        return ret

def ExceptionOccurred():
    init()
    exception = Jni.jenv.ExceptionOccurred(Jni.p_jenv)
    if(exception):
        print("Exception occurred")
    return exception

def ExceptionClear():
    init()
    Jni.jenv.ExceptionClear(Jni.p_jenv)

def argsToJvalueArray(args):
    length = len(args)
    values = []
    for a in args:
        jv = jvalue()
        if(isinstance(a, bool)):
            jv.z = a
        elif(isinstance(a, c_byte)):
            jv.b = a
        elif(isinstance(a, c_char)):
            jv.c = a
        elif(isinstance(a, c_short)):
            jv.s = a
        elif(isinstance(a, int)):
            jv.i = a
        elif(isinstance(a, c_long)):
            jv.j = a
        elif(isinstance(a, float)):
            jv.f = a
        elif(isinstance(a, c_double)):
            jv.d = a
        elif(isinstance(a, str)):
            jv.l = NewString(a.encode('utf-8'), len(a))
        elif(isinstance(a, jobject)):
            jv.l = a
        values.append(jv)
    jvalues = None
    if(length > 0):
        jvalues = (jvalue * length)(*values)
    return jvalues
