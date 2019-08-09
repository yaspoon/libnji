from ctypes import *
import pdb

#__all__ = ['JavaVMOption', 'JavaVMInitArgs', 'jobject', 'jclass', 'jthrowable', "jstring", "jarray", "jobjectArray", "jmethodID", "jfieldID", "jvalue", "JNINativeInterface", "JNIEnv", "Jni"]

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
            ("CallBooleanMethodA", c_void_p), #39

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
            ("CallIntMethodA", c_void_p), #51

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

            ("CallStaticBooleanMethod", c_void_p),
            ("CallStaticBooleanMethodV", c_void_p),
            ("CallStaticBooleanMethodA", c_void_p),

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

            ("NewString", c_void_p), #163
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

class Jni:
    library_path = '/usr/lib/jvm/java-8-openjdk/jre/lib/amd64/server/libjvm.so'
    isInit = False
    libjvm = None
    p_jenv = POINTER(JNIEnv)
    jenv = JNIEnv
    jvm = c_void_p

#Do init
def init():
    if(not Jni.isInit):
        Jni.libjvm = cdll.LoadLibrary(Jni.library_path)

        JNI_CreateJavaVM = getattr(Jni.libjvm, 'JNI_CreateJavaVM')

        JNI_CreateJavaVM.argtypes = [POINTER(c_void_p), POINTER(c_void_p), POINTER(JavaVMInitArgs)]
        JNI_CreateJavaVM.restype = c_int

        jvm = c_void_p(None)
        p_jenv = c_void_p(None)

        OneVmOption = JavaVMOption * 1
        vm_options = OneVmOption()
        vm_options[0].optionString = c_char_p('-Xrs')

        #print(vm_options)
        vm_args = JavaVMInitArgs()
        vm_args.version = 0x00010004
        vm_args.nOptions = 0
        #vm_args.options = cast(pointer(vm_options), POINTER(JavaVMOption))
        vm_args.options = cast(None, POINTER(JavaVMOption))
        vm_args.ignoreUnrecognized = c_bool(True)

        ret = JNI_CreateJavaVM(byref(jvm), byref(p_jenv), byref(vm_args))
        Jni.jvm = jvm

        #Cast void pointer into JNIEnv* aka JNINativeInterface**
        Jni.p_jenv = cast(p_jenv, POINTER(JNIEnv))
        print("addressof(p_jenv):" + hex(addressof(p_jenv)))

        #Get underlying object aka deref pointer
        jenv = Jni.p_jenv.contents # JNINativeInterface *
        Jni.jenv = jenv.contents #JNINativeInterface
        Jni.isInit = True

def GetVersion():
    init()
    return Jni.jenv.GetVersion(Jni.p_jenv)

def FindClass(fqname):
    init()
    return Jni.jenv.FindClass(Jni.p_jenv, fqname)

def GetMethodID(Class, name, sig):
    init()
    return Jni.jenv.GetMethodID(Jni.p_jenv, Class, name, sig)

def CallObjectMethod(obj, method, *args):
    init()
    return Jni.jenv.CallObjectMethod(Jni.p_jenv, obj, method)

def GetArrayLength(array):
    init()
    return Jni.jenv.GetArrayLength(Jni.p_jenv, array)

def GetObjectArrayElement(array, index):
    init()
    return Jni.jenv.GetObjectArrayElement(Jni.p_jenv, array, index)

def GetStringUTFChars(string, isCopy):
    init()
    c_str = Jni.jenv.GetStringUTFChars(Jni.p_jenv, string, isCopy)
    return c_str

def CallIntMethod(obj, method, *args):
    init()
    return Jni.jenv.CallIntMethod(Jni.p_jenv, obj, method)

def CallBooleanMethod(obj, method, *args):
    init()
    return Jni.jenv.CallBooleanMethod(Jni.p_jenv, obj, method)

def ReleaseStringUTFChars(string, c_str):
    init()
    Jni.jenv.ReleaseStringUTFChars(Jni.p_jenv, string, c_str)
