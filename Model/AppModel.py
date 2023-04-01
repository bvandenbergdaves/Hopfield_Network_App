import numpy as np
import os
from Model.Processes import ToGreyscale, ToOneBit, AddNoise, Crop, Compress, ScaleUp, MakeNetwork, MakeAnimation
from Model.functions.imToRgb import getImages
from Model.functions.RgbToIm import saveImages
from Model.functions.main import generatePatterns, makeNetwork, saveNetwork


class MainApp:
    def __init__(self) -> None:
        self.options = ['Edit Images', 'Hopfield Networks']
    
    def is_valid_option(self,value: int):
        try:
            int(value)
        except:
            return False
        index = int(value) - 1
        if index < 0 or len(self.options) <= index:
            return False
        return True

    def get_option(self, value):
        return self.options[int(value) - 1]

class FolderInputApp:
    def __init__(self, app_choice) -> None:
        self.app_choice = app_choice
        self.image_folder = None
        self.save_folder = None

    def set_image_folder(self, value):
        if not os.path.isdir(value):
            return 'Please enter a valid directory path.'
        else:
            self.image_folder = value
    
    def set_save_folder(self, value):
        if not os.path.isdir(value):
            return 'Please enter a valid directory path.'
        else:
            self.save_folder = value
    
    def reset_field(self, field_name):
        if field_name == 'Import Folder':
            self.image_folder = None
        elif field_name == 'Save Folder':
            self.save_folder = None

class ProcessImagesApp:
    def __init__(self, image_folder, save_folder, rgbs = None) -> None:
        self.image_folder = image_folder
        self.save_folder = save_folder
        self.options = ['Convert to greyscale', 'Convert to one-bit', 'Add noise',
                        'Crop', 'Compress', 'Scale up']
        if rgbs is None:
            self.image_batch = getImages(image_folder)
        else:
            self.image_batch = rgbs
        self.process = None
    
    def is_valid_option(self,value):
        try:
            int(value)
        except:
            return False
        index = int(value) - 1
        if index < 0 or len(self.options) <= index:
            return False
        return True
    
    def get_option(self, value):
        return self.options[int(value) - 1]

    def start_process(self, process_name):
        if process_name == 'Convert to greyscale':
            self.process = ToGreyscale()
        elif process_name == 'Convert to one-bit':
            self.process = ToOneBit()
        elif process_name == 'Add noise':
            self.process = AddNoise()
        elif process_name == 'Crop':
            self.process = Crop()
        elif process_name == 'Compress':
            self.process = Compress()
        elif process_name == 'Scale up':
            self.process = ScaleUp()
        
    def get_process_args(self):
        if self.process is not None:
            return self.process.arg_names
        
    def set_field(self, field, value):
        return self.process.set_value(field, value)

    def reset_field(self, field_name):
        self.process.reset_value(field_name)

    def run_process(self):
        processed_batch = []
        for rgb in self.image_batch:
            processed_batch.append(self.process.run(rgb))
        self.image_batch = processed_batch

    def save_batch(self):
        saveImages(self.image_batch, self.save_folder)

    
    def generate_patterns(self):
        self.patterns = generatePatterns(self.image_folder, (self.height, self.width), self.cutoff)

    def initialize_network(self):
        self.network = makeNetwork(self.patterns, self.density, (self.height, self.width))

    def save_network(self):
        saveNetwork(self.network, self.network_name, self.save_folder)

class NetworkApp:
    def __init__(self, image_folder, save_folder) -> None:
        self.image_folder = image_folder
        self.save_folder = save_folder
        self.options = ['Make Network', 'Make Animations from Network']
        self.process = None
    
    def is_valid_option(self,value):
        try:
            int(value)
        except:
            return False
        index = int(value) - 1
        if index < 0 or len(self.options) <= index:
            return False
        return True
    
    def get_option(self, value):
        return self.options[int(value) - 1]

    def start_process(self, process_name):
        if process_name == 'Make Network':
            self.process = MakeNetwork()
        elif process_name == 'Make Animations from Network':
            self.process = MakeAnimation()
        
    def get_process_args(self):
        if self.process is not None:
            return self.process.arg_names
        
    def set_field(self, field, value):
        return self.process.set_value(field, value)

    def reset_field(self, field_name):
        self.process.reset_value(field_name)
    
    def save_batch(self):
        pass


    def run_process(self):
        self.process.run(self.image_folder, self.save_folder)

    
    