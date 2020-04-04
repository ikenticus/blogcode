# https://bytes.com/topic/python/answers/792283-calling-variable-function-name

import sys


class Transforms(object):
    def run_A(self, *args):
        print("run_%s %s %s" % args)

    def run_B(self, *args):
        print("run_%s %s %s" % args)

    def run_C(self, *args):
        print("run_%s %s %s" % args)

    def run_D(self, *args):
        print("run_%s %s %s" % args)

    def defaultTransform(self, *args):
        print("Transform %s not recognised" % args[0])

    def doCommand(self, cmd, *args):
        cmdargs = [cmd] + list(args)
        return getattr(self, 'run_'+cmd, self.defaultTransform)(*cmdargs)

transforms = Transforms()
result = transforms.doCommand(sys.argv[1], 'alpha', 'beta')


class MyFunctions(object):
    def funcA(self, param1, param2):
        print("FA " + param1 + " " + param2)

    def funcB(self, param1, param2):
        print("FB " + param1 + " " + param2)

    def funcC(self, param1, param2):
        print("FC " + param1 + " " + param2)

    def defaultFunc(self, *args):
        print("Command not recognised")

    def doCommand(self, cmd, *args):
        return getattr(self, 'func'+cmd, self.defaultFunc)(*args)

functions = MyFunctions()
result = functions.doCommand(sys.argv[1], 'foo', 'bar')


def FA(param1,param2):
    print("FA " + param1 + " " + param2)

def FB(param1,param2):
    print("FB " + param1 + " " + param2)

def FC(param1,param2):
    print("FC " + param1 + " " + param2)

temp = sys.argv[1]
func = globals()["F" + temp]
func("Hello", "World")

