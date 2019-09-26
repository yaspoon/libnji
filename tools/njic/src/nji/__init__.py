#!/usr/bin/python

from .jni import *
from .javap import *
from .pyjavap import *
from jinja2 import Template
import json
import os
import io
import sys
from multiprocessing import Pool
from multiprocessing import Process
from multiprocessing import Manager


__all__ = [
    'template_h',
    'template_c',
    'parse',
    'parse_nji',
]


# default locations for templates
_root = os.path.dirname(__file__)
_templates = os.path.join(_root, 'templates')
template_h = os.path.join(_templates, 'default.h')
template_c = os.path.join(_templates, 'default.c')


def _nji_to_class(data):
    """Parse an NJI file and return a JniClass"""

    name = data.pop('class')
    fields = data.pop('fields', [])
    constructors = data.pop('constructors', [])
    methods = data.pop('methods', [])

    clazz = JniClass(name, **data)

    # fields
    if isinstance(fields, list):
        for field in fields:
            name = field.pop('name')
            field.setdefault('flags', 0)
            if field.pop('static', False):
                field['flags'] |= JniField.FLAG_STATIC
            if field.pop('optional', False):
                field['flags'] |= JniField.FLAG_OPTIONAL
            JniField(name, **field).add_to(clazz)
    elif fields == '*':
        clazz.fields = JniAll

    # constructors
    if isinstance(constructors, list):
        for constructor in constructors:
            constructor.setdefault('flags', 0)
            if constructor.pop('optional', False):
                constructor['flags'] |= JniConstructor.FLAG_OPTIONAL
            JniConstructor(clazz.shortname, **constructor).add_to(clazz)
    elif constructors == '*':
        clazz.constructors = JniAll

    # methods
    if isinstance(methods, list):
        for method in methods:
            name = method.pop('name')
            method.setdefault('flags', 0)
            if method.pop('static', False):
                method['flags'] |= JniMethod.FLAG_STATIC
            if method.pop('optional', False):
                method['flags'] |= JniMethod.FLAG_OPTIONAL
            JniMethod(name, **method).add_to(clazz)
    elif methods == '*':
        clazz.methods = JniAll

    return clazz


def _javap_to_class(data, classpath=None, use_pyjavap=False):
    """Parse the output of javap for a java class and return a JniClass"""

    classname = data['class']

    # build classpath
    classpath = classpath or []
    extra = data.get('classpath')
    if extra:
        if isinstance(extra, list):
            classpath.extend(extra)
        else:
            classpath.append(extra)

    # parse the complete class
    if(use_pyjavap):
        clazz_full = PyJavaP.parse_class(classname, classpath)
    else:
        clazz_full = JavaP.parse_class(classname, classpath)

    # parse the partial class
    clazz_partial = _nji_to_class(data)

    return JniClass.reduce(clazz_full, clazz_partial)


def _internal_parse(fd, classpath=None, use_pyjavap = False):
    """Parse an NJI file and generate a JniClass based on the NJI file itself
    and any additional information that can be retrieved from javap"""

    data = json.load(fd)
    force = data.get('force', False)

    # create class directly
    if force:
        clazz = _nji_to_class(data)

    # create class using javap
    else:
        clazz = _javap_to_class(data, classpath=classpath, use_pyjavap=use_pyjavap)
        
    if clazz:
        clazz.validate()
        clazz.uniqify()

    return clazz

#Used for multiprocessing with pyjavap
def process_parse(filebytes, classpath=None, use_pyjavap = True):
    clazz = None
    encoded_bytes = filebytes
    if not isinstance(filebytes, bytes):
        encoded_bytes = filebytes.encode('utf8')
    with io.BytesIO(encoded_bytes) as fd:
        clazz = _internal_parse(fd, classpath, use_pyjavap)
    return clazz

pool = None
#Will use multiprocessing for the use_pyjavap=True case to avoid GIL contention when multithreading
def parse(fd, classpath=None, use_pyjavap = False, SCONS_AWEFUL_HACK = False):
    global pool
    if pool is None:
        if SCONS_AWEFUL_HACK is True:
            #Oh god scons2 why do you have to be this way...
            #See https://stackoverflow.com/questions/24453387/scons-attributeerror-builtin-function-or-method-object-has-no-attribute-disp
            #This is only needed on Ubuntu 18.04s SCons 3.0.1 which does nasty things to pickle and cPickle SIGH
            import imp

            del sys.modules['pickle']
            del sys.modules['cPickle']

            sys.modules['pickle'] = imp.load_module('pickle', *imp.find_module('pickle'))
            sys.modules['cPickle'] = imp.load_module('cPickle', *imp.find_module('cPickle'))

            import pickle
            import cPickle
        pool = Pool(processes=4)

    clazz = None
    if use_pyjavap is True:
        filebytes = fd.read()
        clazz = pool.apply(process_parse, args=(filebytes, classpath, use_pyjavap))
    else:
        clazz = _internal_parse(fd, classpath, use_pyjavap)
    return clazz


def _internal_parse_nji(source, output_c, output_h, classpath=None, use_pyjavap=False):
    # parse
    try:
        with open(source, 'rb') as source_fd:
            clazz = _internal_parse(source_fd, classpath=classpath, use_pyjavap=use_pyjavap)
    except Exception as e:
        sys.stderr.write('%s\n' % e)
        return -2

    include = os.path.relpath(os.path.abspath(output_h), os.path.dirname(os.path.abspath(output_c)))

    # output header
    with open(template_h, 'rb') as template_h_fd:
        jinja_template_h = Template(template_h_fd.read().decode('utf-8'))
        with open(output_h, 'wb') as output_h:
            output_h.write(jinja_template_h.render(cls=clazz).encode('utf-8'))
    # output source
    with open(template_c, 'rb') as template_c_fd:
        jinja_template_c = Template(template_c_fd.read().decode('utf-8'))
        with open(output_c, 'wb') as output_c:
            output_c.write(jinja_template_c.render(cls=clazz, include=include).encode('utf-8'))

def parse_nji(source, output_c, output_h, classpath=None, use_pyjavap=False, SCONS_AWEFUL_HACK=False):
    global pool
    if pool is None:
        if SCONS_AWEFUL_HACK is True:
            #Oh god scons2 why do you have to be this way...
            #See https://stackoverflow.com/questions/24453387/scons-attributeerror-builtin-function-or-method-object-has-no-attribute-disp
            #This is only needed on Ubuntu 18.04s SCons 3.0.1 which does nasty things to pickle and cPickle SIGH
            import imp

            del sys.modules['pickle']
            del sys.modules['cPickle']

            sys.modules['pickle'] = imp.load_module('pickle', *imp.find_module('pickle'))
            sys.modules['cPickle'] = imp.load_module('cPickle', *imp.find_module('cPickle'))

            import pickle
            import cPickle
        pool = Pool(processes=4)
    #Use multi processing for both pyjavap and javap it speeds up the jinja templating
    pool.apply(_internal_parse_nji, args=(source, output_c, output_h, classpath, use_pyjavap))
