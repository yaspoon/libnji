from .jenv import *

def fromFullyQualifiedName(fqname):
    from . import Class
    Class.class_init()
    self = Class.Class()
    self.fqname = fqname
    self.Class = FindClass(self.fqname)
    if(not self.Class):
        raise IOError("Failed to find class:{}".format(fqname))
    self.constructors = None
    self.methods = None
    self.fields = None
    return self

def fromJclass(class_obj):
    from . import Class
    Class.class_init()
    self = Class.Class()

    fqname = str(Class._getName(class_obj))
    if(not Class._isArray(class_obj) and not Class._isPrimitive(class_obj)):
            fqname = "L{};".format(fqname)
            fqname = fqname.replace('.', '/')

    self.fqname = fqname
    self.Class = class_obj

    return self
