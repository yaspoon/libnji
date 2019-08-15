from ctypes import *
from .jenv import *

class String(str):
    def __init__(self, jstring):
        self.jstring = jstring
        self.string = None

    def __str__(self):
        if(not self.string):
            c_str = GetStringUTFChars(self.jstring, False)
            self.string = cast(c_str, c_char_p).value.decode('utf-8')
            ReleaseStringUTFChars(self.jstring, c_str)
        return self.string

    def __unicode__(self):
        return u'{}'.format(str(self).encode('utf-8'))

    def __eq__(self, other):
        if(isinstance(other, str)):
            return str(self) == other
        elif(hasattr(other, '__str__')):
            return str(self) == str(other)
        else:
            return NotImplemented

    def __ne__(self, other):
        if(isinstance(other, str)):
            return str(self) != other
        elif(hasattr(other, '__str__')):
            return str(self) != str(other)
        else:
            return NotImplemented

    def __del__(self):
        if(self.jstring != None):
            DeleteLocalRef(self.jstring)
