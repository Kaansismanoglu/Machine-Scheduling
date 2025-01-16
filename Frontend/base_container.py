import customtkinter

# Container class to group related widgets
class Container(customtkinter.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)