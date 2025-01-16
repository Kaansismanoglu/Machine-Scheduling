import customtkinter
from base_container import Container
from Backend.Single.Dispatcing.Dispatching import Dispatching_Calculator


class TabContainer(Container):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid(row=0, column=1, columnspan=1, padx=10, pady=10)
        
        self.tabview = customtkinter.CTkTabview(self, width=500)
        self.tabview.grid(row=0, column=3, padx=(20, 0), pady=(20, 0))
        
        # Add tabs
        self.tabs = ["Single Dispatching Rules"]
        for tab in self.tabs:
            self.tabview.add(tab)
            self.tabview.tab(tab).grid_columnconfigure(0, weight=1)
            
        # Gamma tab content
        self.gamma_menu = customtkinter.CTkOptionMenu(self.tabview.tab("Single Dispatching Rules"),
                                                     dynamic_resizing=False,
                                                     values=["SPT (1| |∑C_j)", "LPT (1| |∑C_j)", "EDD (1| |Lmax)", "WSPT (1| |∑w_j*C_j)", "SRPT (1|r_j, Pmtn|∑C_j)"],
                                                     width=300)
        self.gamma_menu.grid(row=0, column=0, columnspan=2, padx=5, pady=(20, 5))
        
        
        # File selection
        self.file_label2 = customtkinter.CTkLabel(self.tabview.tab("Single Dispatching Rules"),
                                                text="Select Data File:",
                                                anchor="w")
        self.file_label2.grid(row=1, column=0, padx=5, pady=(20,5), sticky="w")
        
        self.file_button2 = customtkinter.CTkButton(self.tabview.tab("Single Dispatching Rules"),
                                                  text="Browse File",
                                                  command=self.select_file)
        self.file_button2.grid(row=1, column=1, padx=5, pady=(20,5))
        
        
        # Start button
        self.main_button = customtkinter.CTkButton(self, 
                                                  fg_color="transparent",
                                                  border_width=2,
                                                  text_color=("gray10", "#DCE4EE"),
                                                  text="Calculate & Show Results",
                                                  command=self.calculate_results,
                                                  font=customtkinter.CTkFont(weight="bold", size=12))
        self.main_button.grid(row=3, column=4, padx=(20, 20), pady=(20, 20))
        
        
    # File selection
    def select_file(self):
        file_path = customtkinter.filedialog.askopenfilename(
            title="Select Data File",
            filetypes=[("Excel files", "*.xlsx")]
        )
        if file_path:
            self.selected_file = file_path
            
            
    def calculate_results(self):
        selected_rule = self.gamma_menu.get()
        metrics = Dispatching_Calculator(self.selected_file, selected_rule)