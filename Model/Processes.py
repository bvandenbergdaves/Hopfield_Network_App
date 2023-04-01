from Model.functions.rgbArrays import *
from Model.functions.main import makeNetworkFromFolder, makeNetworkAnimation
from functools import partial


class Argument:
    def __init__(self, name, constraint, converter, error) -> None:
        self.name = name
        self.value = None
        self.constraint = constraint
        self.converter = converter
        self.error = error
    
    def set_value(self, value):
        if self.constraint(value):
            self.value = self.converter(value)
        else:
            return self.error
    
    def reset_value(self):
        self.value = None


class RgbProcess:
    def __init__(self, func, args) -> None:
        self.func = func
        self.args = args
    
    @property
    def arg_names(self):
        return [arg.name for arg in self.args]
    
    @property
    def arg_dict(self):
        result = dict()
        for arg in self.args:
            result[arg.name] = arg.value
        return result

    def set_value(self, name, value):
        for arg in self.args:
            if arg.name == name:
                return arg.set_value(value)
    
    def reset_value(self, name):
        for arg in self.args:
            if arg.name == name:
                return arg.reset_value()

    def run(self, rgb):
        return self.func(rgb, **self.arg_dict)

class ToGreyscale(RgbProcess):
    def __init__(self) -> None:
        func = toGreyscale
        args = []
        super().__init__(func, args)

class ToOneBit(RgbProcess):
    def __init__(self) -> None:
        func = toOneBit
        args = []
        super().__init__(func, args)

class AddNoise(RgbProcess):
    def __init__(self) -> None:
        func = addRgbNoise
        args = [Argument('sigma', partial(check_float, minimum = 0, maximum = 1000),
                         float,'Sigma must be between 0 and 1000')]
        super().__init__(func, args)

class Crop(RgbProcess):
    def __init__(self) -> None:
        func = shapeCrop
        args = [Argument('width', check_int, int, 'Please enter an integer value'),
                Argument('height', check_int, int, 'Please enter an integer value'),
                Argument('refPt', ref_pt_checker, lambda x : x,
                         'Enter one for the following: top left, '
                         + 'top right, bottom left, bottom right, center')]
        super().__init__(func, args)

class Compress(RgbProcess):
    def __init__(self) -> None:
        func = compress
        args = [Argument('pxSize', check_int, int, 'Please enter an integer value')]
        super().__init__(func, args)

class ScaleUp(RgbProcess):
    def __init__(self) -> None:
        func = scaleUp
        args = [Argument('scale', partial(check_int, minimum = 0), int,
                         'Please enter an integer value')]
        super().__init__(func, args)


class NetworkProcess:
    def __init__(self, func, args) -> None:
        self.func = func
        self.args = args
    
    @property
    def arg_names(self):
        return [arg.name for arg in self.args]
    
    @property
    def arg_dict(self):
        result = dict()
        for arg in self.args:
            result[arg.name] = arg.value
        return result

    def set_value(self, name, value):
        for arg in self.args:
            if arg.name == name:
                return arg.set_value(value)
    
    def reset_value(self, name):
        for arg in self.args:
            if arg.name == name:
                return arg.reset_value()

    def run(self, import_folder, save_folder):
        return self.func(import_folder, save_folder, **self.arg_dict)

class MakeNetwork(NetworkProcess):
    def __init__(self) -> None:
        func = makeNetworkFromFolder
        args = [Argument('width', partial(check_int, minimum = 10, maximum = 100),
                         int, 'Please enter an integer value between 10 and 100'),
                Argument('height', partial(check_int, minimum = 10, maximum = 100),
                         int, 'Please enter an integer value between 10 and 100'),
                Argument('cutoff', partial(check_float, minimum = 0.2, maximum = 0.5),
                         float, 'Please enter a decimal value bewteen 0.3 and 0.5'),
                Argument('density', partial(check_float, minimum = 0.2, maximum = 1),
                         float, 'Please enter a decimal value bewteen 0.2 and 1'),
                Argument('name', lambda x : True, lambda x : x, 'Network Name')]
        super().__init__(func, args)

class MakeAnimation(NetworkProcess):
    def __init__(self) -> None:
        func = makeNetworkAnimation
        args = [Argument('network_name', lambda x : True, lambda x : x, 'Network Name'),
                Argument('pattern_number', partial(check_int, minimum = 0),
                         int, 'Please enter the number of a pattern for the desired network'),
                Argument('tempurature', partial(check_float, minimum = 0, maximum = 0.4),
                         float, 'Please enter a decimal value between 0 and 0.4'),
                Argument('noise', partial(check_float, minimum = 0, maximum = 0.4),
                         float, 'Please enter a decimal value between 0 and 0.4'),
                Argument('number_of_iterations', partial(check_int, minimum = 1, maximum = 7000),
                         int, 'Please enter an integer value bewteen 1 and 7000'),
                Argument('sample_rate', partial(check_int, minimum = 1, maximum = 100),
                         int, 'Please enter a decimal value bewteen 1 and 100'),
                Argument('fps', partial(check_int, minimum = 1, maximum = 10),
                         int, 'Please enter a decimal value bewteen 1 and 10'),]
        super().__init__(func, args)


def ref_pt_checker(value):
    if value in ['top left', 'top right', 'bottom left', 'bottom right', 'center']:
        return True
    return False

def check_int(value, minimum = None, maximum = None):
    try:
        int(value)
    except:
        return False
    if minimum is not None and int(value) < minimum:
        return False
    if maximum is not None and maximum < int(value):
        return False
    return True

def check_float(value, minimum = None, maximum = None):
    try:
        float(value)
    except:
        return False
    if minimum is not None and float(value) < minimum:
        return False
    if maximum is not None and maximum < float(value):
        return False
    return True