import customtkinter
from base_container import Container
from Backend.Flowshop.Approximation.Approximation import Flow_Shop_Approximation_Algorithms


class FlowShop_Approximation_Container(Container):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid(row=0, column=1, columnspan=1, padx=10, pady=10)
        
        self.tabview6 = customtkinter.CTkTabview(self, width=500)
        self.tabview6.grid(row=0, column=3, padx=(20, 0), pady=(20, 0))
        
        # Add tabs
        self.tabs = ["Flow Shop Approximation"]
        for tab in self.tabs:
            self.tabview6.add(tab)
            self.tabview6.tab(tab).grid_columnconfigure(0, weight=1)
            
        # Gamma tab content
        self.gamma_menu6 = customtkinter.CTkOptionMenu(self.tabview6.tab("Flow Shop Approximation"),
                                                     dynamic_resizing=False,
                                                     values=["Decomposition Algorithm (m/2)", "Aggregation Algorithm (m/2)"],
                                                     width=300)
        self.gamma_menu6.grid(row=0, column=0, columnspan=2, padx=5, pady=(20, 5))
        
        
        # File selection
        self.file_label6 = customtkinter.CTkLabel(self.tabview6.tab("Flow Shop Approximation"),
                                                text="Select Data File:",
                                                anchor="w")
        self.file_label6.grid(row=1, column=0, padx=5, pady=(20,5), sticky="w")
        
        self.file_button6 = customtkinter.CTkButton(self.tabview6.tab("Flow Shop Approximation"),
                                                  text="Browse File",
                                                  command=self.select_file)
        self.file_button6.grid(row=1, column=1, padx=5, pady=(20,5))
        
        # Machine count input
        self.machine_count_label6 = customtkinter.CTkLabel(self.tabview6.tab("Flow Shop Approximation"), 
                                                     text="Number of Machines:",
                                                     anchor="w")
        self.machine_count_label6.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        
        self.machine_count_entry6 = customtkinter.CTkEntry(self.tabview6.tab("Flow Shop Approximation"),
                                                     width=100)
        self.machine_count_entry6.grid(row=2, column=1, padx=5, pady=5)
        
        
        # Start button
        self.main_button6 = customtkinter.CTkButton(self, 
                                                  fg_color="transparent",
                                                  border_width=2,
                                                  text_color=("gray10", "#DCE4EE"),
                                                  text="Calculate & Show Results",
                                                  command=self.calculate_results,
                                                  font=customtkinter.CTkFont(weight="bold", size=12))
        self.main_button6.grid(row=3, column=4, padx=(20, 20), pady=(20, 20))
        
        
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
        selected_rule = self.gamma_menu6.get()
        machine_count = int(self.machine_count_entry6.get())
        
        metrics = Flow_Shop_Approximation_Algorithms(self.selected_file, machine_count, selected_rule)