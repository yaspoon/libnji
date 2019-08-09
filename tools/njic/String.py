from ctypes import *
from jni import *

class String(object):
    def __init__(self, jstring):
        self.jstring = jstring
        self.string = None

    def __str__(self):
        if(not self.string):
            c_str = GetStringUTFChars(self.jstring, False)
            self.string = cast(c_str, c_char_p).value
            ReleaseStringUTFChars(self.jstring, c_str)
        return self.string
