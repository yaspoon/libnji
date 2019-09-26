import SCons.Tool
import SCons.Util
import os
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

def parse_nji(target, source, env):
    # parse
    if(len(source) > 0 and len(target) > 0):
        try:
            with open(SCons.Util.to_String(source[0]), 'rb') as source_fd:
                clazz = nji.parse(source_fd, classpath=env['NJICCLASSPATH'], use_pyjavap=env['NJIUSEPYJAVAP'])
        except Exception as e:
            sys.stderr.write('%s\n' % e)
            return -2
        
        # default output source
        output_c = os.path.splitext(SCons.Util.to_String(source[0]))[0] + '.c'

        # default output header
        output_h = os.path.splitext(output_c)[0] + '.h' 

        include = os.path.relpath(os.path.abspath(output_h), os.path.dirname(os.path.abspath(output_c)))

        # output header
        #template_h = Template(args.template_h.read().decode('utf-8'))
        with open(nji.template_h, 'rb') as template_h_fd:
            template_h = Template(template_h_fd.read().decode('utf-8'))
            with open(output_h, 'wb') as output_h:
                output_h.write(template_h.render(cls=clazz).encode('utf-8'))
        # output source
        #template_c = Template(args.template_c.read().decode('utf-8'))
        with open(nji.template_c, 'rb') as template_c_fd:
            template_c = Template(template_c_fd.read().decode('utf-8'))
            with open(output_c, 'wb') as output_c:
                output_c.write(template_c.render(cls=clazz, include=include).encode('utf-8'))

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
