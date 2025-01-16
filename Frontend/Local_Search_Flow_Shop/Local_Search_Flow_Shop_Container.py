import customtkinter
from tkinter import messagebox
from base_container import Container
from Backend.Local_Search.Local_Search_Flow_Shop import Local_Search_Calculator

class TabContainer_Local_Search_Flow_Shop(Container):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid(row=0, column=1, columnspan=1, padx=10, pady=10)
        
        # Create main scrollable frame
        self.main_frame = customtkinter.CTkScrollableFrame(self, width=620, height=500)
        self.main_frame.grid(row=0, column=2, padx=(20, 0), pady=(20, 0))
        
        self.tabview7 = customtkinter.CTkTabview(self.main_frame, width=600)
        self.tabview7.grid(row=0, column=1, padx=(10, 0), pady=(10, 0))
        
        # Add tabs
        self.tabs = ["Local Search for Flow Shop"]
        for tab in self.tabs:
            self.tabview7.add(tab)
            self.tabview7.tab(tab).grid_columnconfigure(0, weight=1)
            
        # Select Objective Function
        self.objective_label7 = customtkinter.CTkLabel(self.tabview7.tab("Local Search for Flow Shop"),
                                                    text="Select Objective Function:",
                                                    anchor="w",
                                                    justify="left")
        self.objective_label7.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        # Objective function options
        self.rule_menu7 = customtkinter.CTkOptionMenu(self.tabview7.tab("Local Search for Flow Shop"),
                                                    dynamic_resizing=False,
                                                    values=["Makespan", "Total Completion Time", "Total Weighted Completion Time", "Total Tardiness", "Total Weighted Tardiness", 
                                                            "Maximum Tardiness", "Number of Tardy Jobs"],
                                                    width=300)
        self.rule_menu7.grid(row=0, column=1, padx=5, pady=(20,5))
        
        # Select Neighbourhood Function
        self.neighbourhood_label7 = customtkinter.CTkLabel(self.tabview7.tab("Local Search for Flow Shop"),
                                                    text="Select Neighbourhood Function:",
                                                    anchor="w",
                                                    justify="left")
        self.neighbourhood_label7.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        
        self.neighbourhood_menu7 = customtkinter.CTkOptionMenu(self.tabview7.tab("Local Search for Flow Shop"),
                                                    dynamic_resizing=False,
                                                    values=["Swap Adjacent"],
                                                    width=300)
        self.neighbourhood_menu7.grid(row=1, column=1, padx=5, pady=(20,5))
        
        # Search idea label
        self.search_idea_label = customtkinter.CTkLabel(self.tabview7.tab("Local Search for Flow Shop"),
                                                    text="Search idea: Move to first improving",
                                                    anchor="w",
                                                    justify="left")
        self.search_idea_label.grid(row=2, column=0, columnspan=2, padx=5, pady=(20,5), sticky="w")
            
        # File selection
        self.file_label7 = customtkinter.CTkLabel(self.tabview7.tab("Local Search for Flow Shop"),
                                                text="Select Data File:",
                                                anchor="w",
                                                justify="left")
        self.file_label7.grid(row=3, column=0, padx=5, pady=(20,5), sticky="w")
        
        self.file_button7 = customtkinter.CTkButton(self.tabview7.tab("Local Search for Flow Shop"),
                                                  text="Browse File",
                                                  command=self.select_file)
        self.file_button7.grid(row=3, column=1, padx=5, pady=(20,5))
        
        # Machine count input
        self.machine_count_label7 = customtkinter.CTkLabel(self.tabview7.tab("Local Search for Flow Shop"), 
                                                     text="Number of Machines:",
                                                     anchor="w",
                                                     justify="left")
        self.machine_count_label7.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        
        self.machine_count_entry7 = customtkinter.CTkEntry(self.tabview7.tab("Local Search for Flow Shop"),
                                                     width=100)
        self.machine_count_entry7.grid(row=4, column=1, padx=5, pady=5)

        # Job count input
        self.job_count_label7 = customtkinter.CTkLabel(self.tabview7.tab("Local Search for Flow Shop"), 
                                                     text="Number of Jobs:",
                                                     anchor="w",
                                                     justify="left")
        self.job_count_label7.grid(row=5, column=0, padx=5, pady=5, sticky="w")
        
        self.job_count_entry7 = customtkinter.CTkEntry(self.tabview7.tab("Local Search for Flow Shop"),
                                                     width=100)
        self.job_count_entry7.grid(row=5, column=1, padx=5, pady=5)

        # Select Iteration or Runtime
        self.iteration_runtime_label = customtkinter.CTkLabel(self.tabview7.tab("Local Search for Flow Shop"),
                                                              text="Select Iteration or Runtime:",
                                                              anchor="w",
                                                              justify="left")
        self.iteration_runtime_label.grid(row=6, column=0, padx=5, pady=(20,5), sticky="w")

        self.iteration_runtime_menu = customtkinter.CTkOptionMenu(self.tabview7.tab("Local Search for Flow Shop"),
                                                                   dynamic_resizing=False,
                                                                   values=["Iterations", "Runtime", "Both"],
                                                                   command=self.toggle_input_fields,
                                                                   width=300)
        self.iteration_runtime_menu.grid(row=6, column=1, padx=5, pady=(20,5))

        # Input for iterations
        self.iteration_label = customtkinter.CTkLabel(self.tabview7.tab("Local Search for Flow Shop"),
                                                       text="Number of Iterations:",
                                                       anchor="w",
                                                       justify="left")
        self.iteration_entry = customtkinter.CTkEntry(self.tabview7.tab("Local Search for Flow Shop"),
                                                       width=100)

        # Input for runtime
        self.runtime_label = customtkinter.CTkLabel(self.tabview7.tab("Local Search for Flow Shop"),
                                                     text="Max Runtime (seconds):",
                                                     anchor="w",
                                                     justify="left")
        self.runtime_entry = customtkinter.CTkEntry(self.tabview7.tab("Local Search for Flow Shop"),
                                                     width=100)

        # Submit button to generate machine and job inputs
        self.submit_button7 = customtkinter.CTkButton(self.tabview7.tab("Local Search for Flow Shop"),
                                                    text="Generate Assignment Interface",
                                                    command=self.generate_assignment_interface)
        self.submit_button7.grid(row=9, column=0, columnspan=2, padx=5, pady=(10,10))
        
        # Frame for machine assignments
        self.assignment_frame7 = customtkinter.CTkFrame(self.tabview7.tab("Local Search for Flow Shop"))
        self.assignment_frame7.grid(row=10, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        
        # Label for assignment instructions
        self.assignment_label7 = customtkinter.CTkLabel(self.assignment_frame7,
                                                   text="Select a job from dropdown and click assign:",
                                                   wraplength=300,
                                                   anchor="w",
                                                   justify="left")
        self.assignment_label7.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        
        # Container for machine frames with horizontal scrolling
        self.machines_container7 = customtkinter.CTkScrollableFrame(self.assignment_frame7, width=500, height=170, orientation="horizontal")  # Increased height for better visibility
        self.machines_container7.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")  # Changed sticky to "nsew" for better layout management

        # Container for job selection
        self.job_selection_frame7 = customtkinter.CTkFrame(self.assignment_frame7, height=50)
        self.job_selection_frame7.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")
        
        # Start button
        self.main_button7 = customtkinter.CTkButton(self, 
                                                  fg_color="transparent", 
                                                  border_width=2,
                                                  text_color=("gray10", "#DCE4EE"),
                                                  text="Calculate & Show Results",
                                                  command=self.calculate_results,
                                                  font=customtkinter.CTkFont(weight="bold", size=12))
        self.main_button7.grid(row=4, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
        
        # Store machine frames and job assignments
        self.machine_frames = []
        self.job_assignments = {}
        self.unassigned_jobs = []
        self.selected_job = None
        
    def toggle_input_fields(self, selection):
        if selection == "Iterations":
            self.iteration_label.grid(row=7, column=0, padx=5, pady=5, sticky="w")
            self.iteration_entry.grid(row=7, column=1, padx=5, pady=5)
            self.runtime_label.grid_forget()
            self.runtime_entry.grid_forget()
        elif selection == "Runtime":
            self.runtime_label.grid(row=7, column=0, padx=5, pady=5, sticky="w")
            self.runtime_entry.grid(row=7, column=1, padx=5, pady=5)
            self.iteration_label.grid_forget()
            self.iteration_entry.grid_forget()
        else:  # Both
            self.iteration_label.grid(row=7, column=0, padx=5, pady=5, sticky="w")
            self.iteration_entry.grid(row=7, column=1, padx=5, pady=5)
            self.runtime_label.grid(row=8, column=0, padx=5, pady=5, sticky="w")
            self.runtime_entry.grid(row=8, column=1, padx=5, pady=5)

    def generate_assignment_interface(self):
        # Clear existing frames
        for frame in self.machine_frames:
            frame[0].destroy()
        self.machine_frames = []
        self.job_assignments = {}
        
        for widget in self.job_selection_frame7.winfo_children():
            widget.destroy()
            
        machine_count = int(self.machine_count_entry7.get())
        job_count = int(self.job_count_entry7.get())
        
        # Initialize unassigned jobs
        self.unassigned_jobs = list(range(1, job_count + 1))
        
        # Create job selection dropdown
        self.job_selection_label7 = customtkinter.CTkLabel(self.job_selection_frame7,
                                                         text="Select Job:",
                                                         anchor="w",
                                                         justify="left")
        self.job_selection_label7.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.job_var7 = customtkinter.StringVar()
        self.job_dropdown7 = customtkinter.CTkOptionMenu(self.job_selection_frame7,
                                                       variable=self.job_var7,
                                                       values=[f"Job {j}" for j in self.unassigned_jobs])
        self.job_dropdown7.grid(row=0, column=1, padx=5, pady=5)
        
        
        # Create frame for each machine
        for m in range(1, 2):
            machine_frame = customtkinter.CTkFrame(self.machines_container7)
            row_pos = ((m-1) // 2) * 2  # Calculate row position for 2 machines per row
            col_pos = (m-1) % 2  # Alternate between columns 0 and 1
            machine_frame.grid(row=row_pos, column=col_pos, padx=5, pady=5, sticky="nsew")
            
            machine_label7 = customtkinter.CTkLabel(machine_frame, 
                                                 text=f"Initial Schedule:",
                                                 font=("Arial", 12, "bold"),
                                                 anchor="w",
                                                 justify="left")
            machine_label7.grid(row=0, column=0, padx=5, pady=5, sticky="w")
            
            assign_button7 = customtkinter.CTkButton(machine_frame,
                                                  text="Assign Job",
                                                  command=lambda m=m: self.assign_to_machine(m))
            assign_button7.grid(row=0, column=1, padx=5, pady=5)
            
            sequence_frame = customtkinter.CTkFrame(machine_frame, height=50)
            sequence_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
            
            # Initialize empty sequence
            self.job_assignments[m] = []
            self.machine_frames.append((machine_frame, sequence_frame))
            
    def assign_to_machine(self, machine_num):
        if not self.job_var7.get():
            return
            
        job_num = int(self.job_var7.get().split()[1])
        
        # Check if job is already assigned
        for machine_jobs in self.job_assignments.values():
            if job_num in machine_jobs:
                return
                
        self.job_assignments[machine_num].append(job_num)
        self.update_machine_displays()
        self.update_job_dropdown()
            
    def update_machine_displays(self):
        for m in self.job_assignments:
            _, sequence_frame = self.machine_frames[m-1]
            
            for widget in sequence_frame.winfo_children():
                widget.destroy()
                
            for i, job in enumerate(self.job_assignments[m]):
                job_label = customtkinter.CTkLabel(sequence_frame,
                                                 text=f"Job {job}",
                                                 width=60,
                                                 height=30,
                                                 anchor="w",
                                                 justify="left")
                job_label.grid(row=0, column=i, padx=2, sticky="w")
                
                remove_btn = customtkinter.CTkButton(sequence_frame,
                                                   text="X",
                                                   width=20,
                                                   command=lambda m=m, j=job: self.remove_job(m, j))
                remove_btn.grid(row=1, column=i, padx=2)
                
    def remove_job(self, machine_num, job_num):
        self.job_assignments[machine_num].remove(job_num)
        self.update_machine_displays()
        self.update_job_dropdown()
        
    def update_job_dropdown(self):
        assigned_jobs = [j for m in self.job_assignments.values() for j in m]
        unassigned = [j for j in self.unassigned_jobs if j not in assigned_jobs]
        
        self.job_dropdown7.configure(values=[f"Job {j}" for j in unassigned])
        if unassigned:
            self.job_var7.set(f"Job {unassigned[0]}")
        else:
            self.job_var7.set("")
            
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
            # Get machine count from entry
            machine_count = int(self.machine_count_entry7.get())
            selected_rule = self.rule_menu7.get()
            
            # Validate all jobs are assigned
            assigned_jobs = [j for m in self.job_assignments.values() for j in m]
            if len(assigned_jobs) != len(self.unassigned_jobs):
                messagebox.showerror("Error", "Please assign all jobs before calculating")
                return
            
            # Get iterations or runtime
            iterations = None
            runtime = None
            
            if self.iteration_runtime_menu.get() == "Iterations":
                iterations = int(self.iteration_entry.get())
            elif self.iteration_runtime_menu.get() == "Runtime":
                runtime = int(self.runtime_entry.get())
            else:  # Both
                iterations = int(self.iteration_entry.get())
                runtime = int(self.runtime_entry.get())
            
            # Call calculation function with file path and job assignments
            metrics = Local_Search_Calculator(selected_rule, self.selected_file, self.job_assignments, machine_count, iterations, runtime)
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during calculation: {str(e)}")