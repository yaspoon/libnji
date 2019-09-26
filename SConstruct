# vi:syntax=python

import os


env = Environment(tools=['default', 'njic'])


# default flags
env.Append(CCFLAGS=['-pedantic', '-Wall'])
env.Append(CPPDEFINES=['__DEBUG__'])
env.Append(CPPPATH=[env.Dir('include')])

#Uncomment below to enable builtin pyjavap when using njic command (maybe faster)
#env['_NJIUSEPYJAVAP'] = '--python-javap'
libnji, test = SConscript('SConscript', exports='env')


# platform specific (change this if required)
JDK_HOME = os.getenv('JDK_HOME', '/usr/lib/jvm/java-8-openjdk')
env.Append(CPPPATH=[os.path.join(JDK_HOME, 'include'), os.path.join(JDK_HOME, 'include', 'linux')])
env.Append(LIBPATH=[os.path.join(JDK_HOME, 'jre', 'lib', 'amd64', 'server')])
env.Append(RPATH=[os.path.join(JDK_HOME, 'lib', 'server')])
env.Append(LIBS=['jvm', 'pthread'])
