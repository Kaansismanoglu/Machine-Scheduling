import customtkinter
from tkinter import messagebox
from base_container import Container
from Backend.Parallel.Dispatching.Parallel_Dispatching import Parallel_Dispacthing_Calculator

class TabContainer_Parallel_Dispatching(Container):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid(row=0, column=1, columnspan=1, padx=20, pady=20)
        
        self.tabview4 = customtkinter.CTkTabview(self, width=500)
        self.tabview4.grid(row=0, column=1, padx=(20, 0), pady=(20, 0))
        
        # Add tabs
        self.tabs = ["Parallel Machine Dispatching Rule"]
        for tab in self.tabs:
            self.tabview4.add(tab)
            self.tabview4.tab(tab).grid_columnconfigure(0, weight=1)
            
        # Dispatching rule selection
        self.rule_label = customtkinter.CTkLabel(self.tabview4.tab("Parallel Machine Dispatching Rule"),
                                                text="Select Dispatching Rule:",
                                                anchor="w")
        self.rule_label.grid(row=0, column=0, padx=5, pady=(20,5), sticky="w")
        
        self.rule_menu = customtkinter.CTkOptionMenu(self.tabview4.tab("Parallel Machine Dispatching Rule"),
                                                    dynamic_resizing=False,
                                                    values=["LPT", "SPT", "Wrap-Around"],
                                                    width=300)
        self.rule_menu.grid(row=0, column=1, padx=5, pady=(20,5))
            
        # File selection
        self.file_label4 = customtkinter.CTkLabel(self.tabview4.tab("Parallel Machine Dispatching Rule"),
                                                text="Select Data File:",
                                                anchor="w")
        self.file_label4.grid(row=1, column=0, padx=5, pady=(20,5), sticky="w")
        
        self.file_button4 = customtkinter.CTkButton(self.tabview4.tab("Parallel Machine Dispatching Rule"),
                                                  text="Browse File",
                                                  command=self.select_file)
        self.file_button4.grid(row=1, column=1, padx=5, pady=(20,5))
        
        # Machine count input
        self.machine_count_label4 = customtkinter.CTkLabel(self.tabview4.tab("Parallel Machine Dispatching Rule"), 
                                                     text="Number of Machines:",
                                                     anchor="w")
        self.machine_count_label4.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        
        self.machine_count_entry4 = customtkinter.CTkEntry(self.tabview4.tab("Parallel Machine Dispatching Rule"),
                                                     width=100)
        self.machine_count_entry4.grid(row=2, column=1, padx=5, pady=5)
        
        # Start button
        self.main_button4 = customtkinter.CTkButton(self, 
                                                  fg_color="transparent", 
                                                  border_width=2,
                                                  text_color=("gray10", "#DCE4EE"),
                                                  text="Calculate & Show Results",
                                                  command=self.calculate_results,
                                                  font=customtkinter.CTkFont(weight="bold", size=12))
        self.main_button4.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
            
    def select_file(self):
        file_path = customtkinter.filedialog.askopenfilename(
            title="Select Data File",
            filetypes=[("Excel files", "*.xlsx")]
        )
        if file_path:
            self.selected_file = file_path
            
    def calculate_results(self):
        # Validate file is selected
        if not hasattr(self, 'selected_file'):
            messagebox.showerror("Error", "Please select a data file first")
            return
            
        try:
            # Get machine count and selected rule
            machine_count = int(self.machine_count_entry4.get())
            selected_rule = self.rule_menu.get()
            
            # Call calculation function with file path, machine count and selected rule
            metrics = Parallel_Dispacthing_Calculator(self.selected_file, machine_count, selected_rule)
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during calculation: {str(e)}")