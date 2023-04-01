import os

class SelectionView:
    def __init__(self, header, options) -> None:
        self.header = header
        self.options = options
        self.prompt = 'Select an option by number: '
        self.error = None

    def display(self):
        os.system('clear')
        print(self.header)
        for i, option in enumerate(self.options):
            print(f'{i+1})  {option}')

        if self.error == None:
            print()
        else:
            print('\nError: ', self.error)
    
    def set_error(self, error):
        self.error = error

class AppSelectionView(SelectionView):
    def __init__(self, options) -> None:
        header = 'Select application'
        super().__init__(header, options)
    
    def display(self, presenter):
        super().display()
        presenter.on_app_choice(input(self.prompt))

class ProcessSelectionView(SelectionView):
    def __init__(self, options) -> None:
        header = 'Select image operation'
        super().__init__(header, options)
    
    def display(self, presenter):
        super().display()
        presenter.on_image_process_choice(input(self.prompt))

class NetworkView(SelectionView):
    def __init__(self, options) -> None:
        header = 'Select network process'
        super().__init__(header, options)
    
    def display(self, presenter):
        super().display()
        presenter.on_network_process_choice(input(self.prompt))

