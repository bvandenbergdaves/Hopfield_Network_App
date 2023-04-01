from View.InputView import FolderInputView, ParameterInputView
from View.SelectionView import AppSelectionView, ProcessSelectionView, NetworkView
from View.DisplayView import MessageView
from Model.AppModel import ProcessImagesApp, MainApp, FolderInputApp, NetworkApp



class Presenter:
    def __init__(self) -> None:
        self.model = MainApp()
        self.view = AppSelectionView(self.model.options)
        self.view.display(self)

    def on_app_choice(self, value):
        if not self.model.is_valid_option(value):
            self.view.set_error('Please enter a valid selection')
            self.view.display(self)
        elif self.model.get_option(value) == 'Edit Images':
            self.model = FolderInputApp('Edit Images')
            self.view = FolderInputView()
            self.view.display(self)
        elif self.model.get_option(value) == 'Hopfield Networks':
            self.model = FolderInputApp('Hopfield Networks')
            self.view = FolderInputView()
            self.view.display(self)
    
    def on_folder_input(self, value):
        if value == 'undo':
            field = self.view.undo()
            self.model.reset_field(field)
        elif value == 'back':
            self.model = MainApp()
            self.view = AppSelectionView(self.model.options)
        elif self.view.is_complete() and self.model.app_choice =='Edit Images':
            self.model = ProcessImagesApp(self.model.image_folder, self.model.save_folder)
            self.view = ProcessSelectionView(self.model.options)
        elif self.view.is_complete() and self.model.app_choice =='Hopfield Networks':
            self.model = NetworkApp(self.model.image_folder, self.model.save_folder)
            self.view = NetworkView(self.model.options)
        else:
            field = self.view.get_field()
            if self.view.get_field() == 'Import Folder':
                error = self.model.set_image_folder(value)
            elif self.view.get_field() == 'Save Folder':
                error = self.model.set_save_folder(value)

            self.view.set_error(error)
            if error is None:
                self.view.set_value(value)
    
        self.view.display(self)
    
    def on_image_process_choice(self, value):
        if not self.model.is_valid_option(value):
            self.view.set_error('Please enter a valid selection')
            self.view.display(self)
        else:
            process = self.model.get_option(value)
            self.model.start_process(process)
            arg_names = self.model.get_process_args()
            if len(arg_names) > 0:
                self.view = ParameterInputView(arg_names)
            else:
                self.model.run_process()
                self.model.save_batch()
                self.view = MessageView('The image operation has finished running.')
        self.view.display(self)
    
    def on_network_process_choice(self, value):
        if not self.model.is_valid_option(value):
            self.view.set_error('Please enter a valid selection')
            self.view.display(self)
        else:
            process = self.model.get_option(value)
            self.model.start_process(process)
            arg_names = self.model.get_process_args()
            if len(arg_names) > 0:
                self.view = ParameterInputView(arg_names)
            else:
                self.model.run_process()
                self.view = MessageView('The network operation has finished running.')
        self.view.display(self)

    def on_parameter_input(self, value):
        if value == 'undo':
            field = self.view.undo()
            self.model.reset_field(field)
        elif value == 'back':
            self.view = ProcessSelectionView(self.model.options)
        elif self.view.is_complete():
            self.model.run_process()
            self.model.save_batch()
            self.view = MessageView('The image operation has finished running.')
        else:
            field = self.view.get_field()
            error = self.model.set_field(field, value)
            self.view.set_error(error)
            if error is None:
                self.view.set_value(value)
    
        self.view.display(self)

    def on_continue(self, _):
        pass
    


