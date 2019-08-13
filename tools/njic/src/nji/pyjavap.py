#!/usr/bin/python

from .jni import *
from . import Class
from .jenv import *


__all__ = ['PyJavaP']


class PyJavaP(object):

    @classmethod
    def parse_class(cls, classname, classpath=None):
        classpath = classpath or []
        clazz = JniClass(classname)

        SetClassPath(classpath)

        fqname = "L{};".format(classname).replace('.', '/')
        cls = Class.fromFullyQualifiedName(fqname)

        if(str(cls.getName()) != clazz.name):
            raise IOError('Bad Class name')

        if(cls):
            for con in cls.getDeclaredConstructors():
                kwargs = {}
                JniConstructor(clazz.shortname, con.descriptor(), **kwargs).add_to(clazz)
            for meth in cls.getDeclaredMethods():
                kwargs = {}
                if(meth.isStatic()):
                    kwargs['flags'] = JniMethod.FLAG_STATIC
                JniMethod(str(meth.getName()), meth.descriptor(), **kwargs).add_to(clazz)
            for field in cls.getDeclaredFields():
                kwargs = {}
                if(field.isStatic()):
                    kwargs['flags'] = JniMethod.FLAG_STATIC
                JniField(str(field.getName()), field.descriptor(), **kwargs).add_to(clazz)
        else:
            raise("Failed to find class:" + fqname)

        return clazz


if __name__ == '__main__':
    import sys
    classpath = sys.argv[1]
    classname = sys.argv[2] if len(sys.argv) > 2 else None
    print(PyJavaP.parse_class(classname, classpath))
