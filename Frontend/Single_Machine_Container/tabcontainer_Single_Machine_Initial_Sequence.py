import customtkinter
from base_container import Container
from Backend.Single.Initial.Initial_Calculator import calculate_initial_metrics

class TabContainer_Initial_Sequence(Container):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid(row=0, column=1, columnspan=1, padx=10, pady=10)
        
        self.tabview2 = customtkinter.CTkTabview(self, width=500)
        self.tabview2.grid(row=0, column=3, padx=(20, 0), pady=(20, 0))
        
        # Add tabs
        self.tabs = ["Single Initial Sequence"]
        for tab in self.tabs:
            self.tabview2.add(tab)
            self.tabview2.tab(tab).grid_columnconfigure(0, weight=1)
            
        # File selection
        self.file_label = customtkinter.CTkLabel(self.tabview2.tab("Single Initial Sequence"),
                                                text="Select Data File:",
                                                anchor="w")
        self.file_label.grid(row=0, column=0, padx=5, pady=(20,5), sticky="w")
        
        self.file_button = customtkinter.CTkButton(self.tabview2.tab("Single Initial Sequence"),
                                                  text="Browse File",
                                                  command=self.select_file)
        self.file_button.grid(row=0, column=1, padx=5, pady=(20,5))
        
        # Job count input
        self.job_count_label = customtkinter.CTkLabel(self.tabview2.tab("Single Initial Sequence"), 
                                                     text="Number of Jobs:",
                                                     anchor="w")
        self.job_count_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        
        self.job_count_entry = customtkinter.CTkEntry(self.tabview2.tab("Single Initial Sequence"),
                                                     width=100)
        self.job_count_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Submit button to generate sequence inputs
        self.submit_button = customtkinter.CTkButton(self.tabview2.tab("Single Initial Sequence"),
                                                    text="Generate Job Numbers",
                                                    command=self.generate_job_numbers)
        self.submit_button.grid(row=2, column=0, columnspan=2, padx=5, pady=(10,10))
        
        # Frame for job sequence
        self.sequence_frame = customtkinter.CTkFrame(self.tabview2.tab("Single Initial Sequence"))
        self.sequence_frame.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        
        # Label for sequence instructions
        self.sequence_label = customtkinter.CTkLabel(self.sequence_frame,
                                                   text="Drag and drop jobs to create sequence:",
                                                   wraplength=300,
                                                   anchor="w")
        self.sequence_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        # Listbox for job sequence
        self.sequence_listbox = customtkinter.CTkTextbox(self.sequence_frame, height=150)
        self.sequence_listbox.grid(row=1, column=0, padx=5, pady=5)
        
        # Start button
        self.main_button = customtkinter.CTkButton(self, 
                                                  fg_color="transparent", 
                                                  border_width=2,
                                                  text_color=("gray10", "#DCE4EE"),
                                                  text="Calculate & Show Results",
                                                  command=self.calculate_results,
                                                  font=customtkinter.CTkFont(weight="bold", size=12))
        self.main_button.grid(row=3, column=4, padx=(20, 20), pady=(20, 20))
        
    def generate_job_numbers(self):
        job_count = int(self.job_count_entry.get())
        job_numbers = list(range(1, job_count + 1))
        self.sequence_listbox.delete("1.0", "end")
        self.sequence_listbox.insert("1.0", "\n".join(str(x) for x in job_numbers))
            
    def select_file(self):
        file_path = customtkinter.filedialog.askopenfilename(
            title="Select Data File",
            filetypes=[("Excel files", "*.xlsx")]
        )
        if file_path:
            self.selected_file = file_path
            
    def calculate_results(self):
        sequence = self.sequence_listbox.get("1.0", "end").split("\n")
        sequence = [int(x) for x in sequence if x.strip()]
        metrics = calculate_initial_metrics(self.selected_file, sequence)