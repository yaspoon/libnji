#!/usr/bin/python


from .jni import *
import subprocess
import re


__all__ = ['PyJavaP']


class PyJavaP(object):

    @classmethod
    def parse_class(cls, classname, classpath=None):
        classpath = classpath or []
        clazz = JniClass(classname)

        return clazz


if __name__ == '__main__':
    import sys
    classpath = sys.argv[1]
    classname = sys.argv[2] if len(sys.argv) > 2 else None
    print(PyJavaP.parse_class(classname, classpath))
