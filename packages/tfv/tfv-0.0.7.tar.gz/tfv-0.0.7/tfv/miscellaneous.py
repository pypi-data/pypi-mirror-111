import inspect
import numpy as np

def dump(obj):
    """
    A function for printing the methods and properties (instance variables) of an object:

        dump(obj)

    :param obj: Any python object
    """
    methods = []
    properties = []

    for attr in dir(obj):
        if hasattr(obj, attr) and '__' not in attr:
            if callable(getattr(obj, attr)):
                methods.append(attr)
            else:
                properties.append(attr)

    print('Methods:')
    for attr in methods:
        print("obj.{}".format(attr))
    print('\nProperties:')
    for attr in properties:
        print("obj.{}".format(attr))


def get_main():
    frames = [stack[0] for stack in inspect.stack()]
    for frame in frames:
        module = inspect.getmodule(frame)
        if module.__name__ == '__main__':
            return module

    return None


def get_object(name):
    module = get_main()
    if hasattr(module, name):
        return getattr(module, name)
    else:
        return None


class Expression:

    @classmethod
    def decorator(cls, function_call):

        def wrapper(*args, **kwargs):
            # Basic preparation
            args = list(args)
            expression = None
            index = None

            # Find expression in input arguments
            for ii, arg in enumerate(args):
                if type(arg).__name__ == cls.__name__:
                    expression, index = arg, ii

            # Evaluate output based on expression
            if expression is None:
                output = function_call(*args, **kwargs)
            else:
                eval_args = list()
                for ii in range(len(expression.variables)):
                    args[index] = expression.variables[ii]
                    if expression.is_defined[ii]:
                        eval_args.append(get_object(args[index]))
                    else:
                        eval_args.append(function_call(*args, **kwargs))
                output = expression.evaluate(*eval_args)

            return output

        return wrapper

    def __init__(self, expression):
        self.expression = expression
        self.__interpret__()

    def __interpret__(self):
        # Define legal operations, functions and characters
        ops = ['**', '*', '/', '+', '-', '>', '<', '=', '|', '&']
        chars = ['[', ']', '(', ')', ' ', "'", ':']
        funcs = ['hyp', 'dot', 'vec', 'sum']
        calls = ['np.hypot', 'np.dot', 'np.column_stack', 'np.sum']

        # Determine variables that exist in expression string
        string = self.expression
        for op in ops:
            string = string.replace(op, ',')
        for other in funcs + chars:
            string = string.replace(other, '')
        self.variables = string.split(',')

        # Remove constants
        for string in self.variables:
            try:
                float(string)
                is_num = True
            except ValueError:
                is_num = False
            if is_num:
                self.variables.remove(string)

        # Remove None types
        for string in self.variables:
            if string == 'None':
                self.variables.remove(string)

        # bug when two operators occur in a row i.e z<-1.0
        for var in self.variables:
            if var == '':
                self.variables.remove(var)

        # Find if any variables that are defined in main name space
        self.is_defined = list()
        for variable in self.variables:
            handle = get_object(variable)
            if handle is None:
                self.is_defined.append(False)
            else:
                self.is_defined.append(True)

        # Determine the evaluation string
        argument_fmt = 'args[{}]'
        self.string = self.expression
        for aa, variable in enumerate(self.variables):
            place_holder = variable
            replace_with = argument_fmt.format(aa)
            self.string = self.string.replace(place_holder, replace_with)
        for aa, func in enumerate(funcs):
            place_holder = func
            replace_with = calls[aa]
            self.string = self.string.replace(place_holder, replace_with)

    def evaluate(self, *args):
        return eval(self.string)


def unsupported_decorator(function_call):

    def wrapper(*args):
        name = function_call.__name__
        message = '{} is currently not supported'.format(name)
        print(message)

    return wrapper



