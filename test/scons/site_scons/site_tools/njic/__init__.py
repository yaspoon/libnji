import SCons.Tool
import SCons.Util
import SCons
import os
import sys
from jinja2 import Template
import nji


__all__ = [
    'exists',
    'generate',
]


NjiAction = SCons.Action.Action('$NJICCOM', '$NJICCOMSTR')


def NjiEmitter(target, source, env):
    targetDir, targetFile = os.path.split(SCons.Util.to_String(target[0]))
    targetName, targetExt = os.path.splitext(targetFile)
    if env['NJICPATHH']:
        targetDir = SCons.Util.to_String(env['NJICPATHH'])
    target.append(os.path.join(targetDir, targetName) + '.h')
    if env['NJICTEMPLATEC']:
        env.Depends(target[0], env['NJICTEMPLATEC'])
    if env['NJICTEMPLATEH']:
        env.Depends(target[1], env['NJICTEMPLATEH'])
    return target, source


class pathopt(object):
    """Copied from javac tool"""
    def __init__(self, opt, var, default=None):
        self.opt = opt
        self.var = var
        self.default = default

    def __call__(self, target, source, env, for_signature):
        path = env[self.var]
        if path and not SCons.Util.is_List(path):
            path = [path]
        if self.default:
            default = env[self.default]
            if default:
                if not SCons.Util.is_List(default):
                    default = [default]
                path = path + default
        if path:
            return [self.opt, os.pathsep.join(map(str, path))]
        else:
            return []

def get_scons_major_minor_rev(version):
    nums = version.split('.')
    major = int(nums[0])
    minor = int(nums[1])
    rev = 0
    if len(nums) is 3:
        rev = int(nums[2])
    return (major, minor, rev)

SCONS_AWEFUL_HACK = None

def parse_nji(target, source, env):
    # parse
    global SCONS_AWEFUL_HACK
    if SCONS_AWEFUL_HACK is None:
        version = get_scons_major_minor_rev(SCons.__version__)
        if version <= (3, 0, 1):
            print("Fixing up old scons with dirty hack")
            SCONS_AWEFUL_HACK = True
        else:
            print("Scons is new and doesn't need dirty hack")
            SCONS_AWEFUL_HACK = False

    if(len(source) > 0 and len(target) > 0):
        #source nji file
        nji_file = SCons.Util.to_String(source[0])

        # default output source
        output_c = os.path.splitext(SCons.Util.to_String(source[0]))[0] + '.c'

        # default output header
        output_h = os.path.splitext(output_c)[0] + '.h' 

        nji.parse_nji(nji_file, output_c, output_h, env['NJICCLASSPATH'], env['NJIUSEPYJAVAP'], SCONS_AWEFUL_HACK)


def generate(env):
    c_file, cxx_file = SCons.Tool.createCFileBuilders(env)
    c_file.add_action('.nji', NjiAction)
    c_file.add_emitter('.nji', NjiEmitter)
    env['NJIC'] = 'njic'
    env['NJICFLAGS'] = SCons.Util.CLVar('')
    env['NJICPATHH'] = None
    env['NJICTEMPLATEC'] = None
    env['NJICTEMPLATEH'] = None
    env['NJICCLASSPATH'] = []
    env['_njicpathopt'] = pathopt
    env['_NJICTEMPLATEC'] = '${_njicpathopt("--template-c", "NJICTEMPLATEC")} '
    env['_NJICTEMPLATEH'] = '${_njicpathopt("--template-h", "NJICTEMPLATEH")} '
    env['_NJICCLASSPATH'] = '${_njicpathopt("--classpath", "NJICCLASSPATH", "JAVACLASSPATH")} '
    env['NJIUSEPYJAVAP'] = True
    env['NJICCOM'] = parse_nji


def exists(env):
    #return env.Detect(['njic'])
    return True
