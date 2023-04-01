import os

class MessageView:
    def __init__(self, message) -> None:
        self.message = message
        self.prompt = 'Press ENTER to continue: '
    
    def display(self,presenter):
        os.system('clear')
        print(self.message)
        presenter.on_continue(input(self.prompt))