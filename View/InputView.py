import os

class InputView:
    def __init__(self, header, fields) -> None:
        self.header = header
        self.fields = fields
        self.prompt = None
        self.field = 0
        self.values = ['' for _ in fields]
        self.error = None

    def display(self):
        os.system('clear')
        print(self.header)
        print('Type \'undo\' to reverse changes')
        for field, value in zip(self.fields, self.values):
            print(field, ': ', value)
        
        if self.error == None:
            print()
        else:
            print('\nError: ', self.error)
        
        if self.field >= len(self.fields):
            self.prompt = 'Press ENTER to continue: '
        else:
            self.prompt = f'Enter a value for {self.fields[self.field]}: '
    
    def undo(self):
        if self.field > 0:
            self.field -= 1
            self.values[self.field] = ''
            return self.fields[self.field] 
    
    def set_error(self, error):
        self.error = error

    def set_value(self,value):
        if not self.is_complete():
            self.values[self.field] = value
            self.field += 1
    
    def is_complete(self):
        return self.field >= len(self.fields)

    def get_field(self):
        if not self.is_complete():
            return self.fields[self.field]

class FolderInputView(InputView):
    def __init__(self) -> None:
        header = 'Select folders to from which to obtain data'
        fields = ['Import Folder', 'Save Folder']
        super().__init__(header, fields)
    
    def display(self, presenter):
        super().display()
        presenter.on_folder_input(input(self.prompt))

class ParameterInputView(InputView):
    def __init__(self, fields) -> None:
        header = 'Enter enter the following parameters'
        super().__init__(header, fields)
    
    def display(self, presenter):
        super().display()
        presenter.on_parameter_input(input(self.prompt))