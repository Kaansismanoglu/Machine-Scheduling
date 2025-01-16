import customtkinter
from base_container import Container
from Backend.Flowshop.Dispatching.Flowshop import Flow_Shop_Algorithms


class FlowShop_Container(Container):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid(row=0, column=1, columnspan=1, padx=10, pady=10)
        
        self.tabview5 = customtkinter.CTkTabview(self, width=500)
        self.tabview5.grid(row=0, column=3, padx=(20, 0), pady=(20, 0))
        
        # Add tabs
        self.tabs = ["Flow Shop Johnson's Algorithm"]
        for tab in self.tabs:
            self.tabview5.add(tab)
            self.tabview5.tab(tab).grid_columnconfigure(0, weight=1)
            
        # Gamma tab content
        self.gamma_menu5 = customtkinter.CTkOptionMenu(self.tabview5.tab("Flow Shop Johnson's Algorithm"),
                                                     dynamic_resizing=False,
                                                     values=["Johnson's Algorithm"],
                                                     width=300)
        self.gamma_menu5.grid(row=0, column=0, columnspan=2, padx=5, pady=(20, 5))
        
        
        # File selection
        self.file_label5 = customtkinter.CTkLabel(self.tabview5.tab("Flow Shop Johnson's Algorithm"),
                                                text="Select Data File:",
                                                anchor="w")
        self.file_label5.grid(row=1, column=0, padx=5, pady=(20,5), sticky="w")
        
        self.file_button5 = customtkinter.CTkButton(self.tabview5.tab("Flow Shop Johnson's Algorithm"),
                                                  text="Browse File",
                                                  command=self.select_file)
        self.file_button5.grid(row=1, column=1, padx=5, pady=(20,5))
        
        #Label for Machine Count
        self.machine_count_label5 = customtkinter.CTkLabel(self.tabview5.tab("Flow Shop Johnson's Algorithm"),
                                                        text="This Algorithm is for 2 Machines",
                                                        anchor="w")
        self.machine_count_label5.grid(row=2, column=0, columnspan=2, padx=5, pady=(20, 5), sticky="w")
        
        # Start button
        self.main_button5 = customtkinter.CTkButton(self, 
                                                  fg_color="transparent",
                                                  border_width=2,
                                                  text_color=("gray10", "#DCE4EE"),
                                                  text="Calculate & Show Results",
                                                  command=self.calculate_results,
                                                  font=customtkinter.CTkFont(weight="bold", size=12))
        self.main_button5.grid(row=3, column=4, padx=(20, 20), pady=(20, 20))
        
        
    # File selection
    def select_file(self):
        file_path = customtkinter.filedialog.askopenfilename(
            title="Select Data File",
            filetypes=[("Excel files", "*.xlsx")]
        )
        if file_path:
            # Get machine count and selected rule
            self.selected_file = file_path
            
            
    def calculate_results(self):
        selected_rule = self.gamma_menu5.get()
        
        metrics = Flow_Shop_Algorithms(self.selected_file)