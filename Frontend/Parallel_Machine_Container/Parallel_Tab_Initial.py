import customtkinter
from tkinter import messagebox
from base_container import Container
from Backend.Parallel.Initial.Parallel_Initial import Parallel_Initial_Calculator

class TabContainer_Parallel_Initial(Container):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid(row=0, column=1, columnspan=1, padx=10, pady=10)
        
        # Create main scrollable frame
        self.main_frame = customtkinter.CTkScrollableFrame(self, width=600, height=500)
        self.main_frame.grid(row=0, column=2, padx=(20, 0), pady=(20, 0))
        
        self.tabview3 = customtkinter.CTkTabview(self.main_frame, width=500)
        self.tabview3.grid(row=0, column=1, padx=(20, 0), pady=(20, 0))
        
        # Add tabs
        self.tabs = ["Parallel Machine Initial Sequence"]
        for tab in self.tabs:
            self.tabview3.add(tab)
            self.tabview3.tab(tab).grid_columnconfigure(0, weight=1)
            
        # File selection
        self.file_label3 = customtkinter.CTkLabel(self.tabview3.tab("Parallel Machine Initial Sequence"),
                                                text="Select Data File:",
                                                anchor="w",
                                                justify="left")
        self.file_label3.grid(row=0, column=0, padx=5, pady=(20,5), sticky="w")
        
        self.file_button3 = customtkinter.CTkButton(self.tabview3.tab("Parallel Machine Initial Sequence"),
                                                  text="Browse File",
                                                  command=self.select_file)
        self.file_button3.grid(row=0, column=1, padx=5, pady=(20,5))
        
        # Machine count input
        self.machine_count_label3 = customtkinter.CTkLabel(self.tabview3.tab("Parallel Machine Initial Sequence"), 
                                                     text="Number of Machines:",
                                                     anchor="w",
                                                     justify="left")
        self.machine_count_label3.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        
        self.machine_count_entry3 = customtkinter.CTkEntry(self.tabview3.tab("Parallel Machine Initial Sequence"),
                                                     width=100)
        self.machine_count_entry3.grid(row=1, column=1, padx=5, pady=5)

        # Job count input
        self.job_count_label3 = customtkinter.CTkLabel(self.tabview3.tab("Parallel Machine Initial Sequence"), 
                                                     text="Number of Jobs:",
                                                     anchor="w",
                                                     justify="left")
        self.job_count_label3.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        
        self.job_count_entry3 = customtkinter.CTkEntry(self.tabview3.tab("Parallel Machine Initial Sequence"),
                                                     width=100)
        self.job_count_entry3.grid(row=2, column=1, padx=5, pady=5)
        
        # Submit button to generate machine and job inputs
        self.submit_button3 = customtkinter.CTkButton(self.tabview3.tab("Parallel Machine Initial Sequence"),
                                                    text="Generate Assignment Interface",
                                                    command=self.generate_assignment_interface)
        self.submit_button3.grid(row=3, column=0, columnspan=2, padx=5, pady=(10,10))
        
        # Frame for machine assignments
        self.assignment_frame3 = customtkinter.CTkFrame(self.tabview3.tab("Parallel Machine Initial Sequence"))
        self.assignment_frame3.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        
        # Label for assignment instructions
        self.assignment_label3 = customtkinter.CTkLabel(self.assignment_frame3,
                                                   text="Select a job from dropdown and click assign:",
                                                   wraplength=300,
                                                   anchor="w",
                                                   justify="left")
        self.assignment_label3.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        # Container for machine frames
        self.machines_container3 = customtkinter.CTkFrame(self.assignment_frame3, height=50)
        self.machines_container3.grid(row=1, column=0, padx=5, pady=5)
        
        # Container for job selection
        self.job_selection_frame3 = customtkinter.CTkFrame(self.assignment_frame3, height=50)
        self.job_selection_frame3.grid(row=2, column=0, padx=5, pady=5)
        
        # Start button
        self.main_button3 = customtkinter.CTkButton(self, 
                                                  fg_color="transparent", 
                                                  border_width=2,
                                                  text_color=("gray10", "#DCE4EE"),
                                                  text="Calculate & Show Results",
                                                  command=self.calculate_results,
                                                  font=customtkinter.CTkFont(weight="bold", size=12))
        self.main_button3.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
        
        # Store machine frames and job assignments
        self.machine_frames = []
        self.job_assignments = {}
        self.unassigned_jobs = []
        self.selected_job = None
        
    def generate_assignment_interface(self):
        # Clear existing frames
        for frame in self.machine_frames:
            frame[0].destroy()
        self.machine_frames = []
        self.job_assignments = {}
        
        for widget in self.job_selection_frame3.winfo_children():
            widget.destroy()
            
        machine_count = int(self.machine_count_entry3.get())
        job_count = int(self.job_count_entry3.get())
        
        # Initialize unassigned jobs
        self.unassigned_jobs = list(range(1, job_count + 1))
        
        # Create job selection dropdown
        self.job_selection_label3 = customtkinter.CTkLabel(self.job_selection_frame3,
                                                         text="Select Job:",
                                                         anchor="w",
                                                         justify="left")
        self.job_selection_label3.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.job_var3 = customtkinter.StringVar()
        self.job_dropdown3 = customtkinter.CTkOptionMenu(self.job_selection_frame3,
                                                       variable=self.job_var3,
                                                       values=[f"Job {j}" for j in self.unassigned_jobs])
        self.job_dropdown3.grid(row=0, column=1, padx=5, pady=5)
        
        # Create frame for each machine
        for m in range(1, machine_count + 1):
            machine_frame = customtkinter.CTkFrame(self.machines_container3)
            row_pos = ((m-1) // 2) * 2  # Calculate row position for 2 machines per row
            col_pos = (m-1) % 2  # Alternate between columns 0 and 1
            machine_frame.grid(row=row_pos, column=col_pos, padx=5, pady=5, sticky="ew")
            
            machine_label3 = customtkinter.CTkLabel(machine_frame, 
                                                 text=f"Machine {m}:",
                                                 font=("Arial", 12, "bold"),
                                                 anchor="w",
                                                 justify="left")
            machine_label3.grid(row=0, column=0, padx=5, pady=5, sticky="w")
            
            assign_button3 = customtkinter.CTkButton(machine_frame,
                                                  text="Assign Job",
                                                  command=lambda m=m: self.assign_to_machine(m))
            assign_button3.grid(row=0, column=1, padx=5, pady=5)
            
            sequence_frame = customtkinter.CTkFrame(machine_frame, height=50)
            sequence_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
            
            # Initialize empty sequence
            self.job_assignments[m] = []
            self.machine_frames.append((machine_frame, sequence_frame))
            
    def assign_to_machine(self, machine_num):
        if not self.job_var3.get():
            return
            
        job_num = int(self.job_var3.get().split()[1])
        
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
        
        self.job_dropdown3.configure(values=[f"Job {j}" for j in unassigned])
        if unassigned:
            self.job_var3.set(f"Job {unassigned[0]}")
        else:
            self.job_var3.set("")
            
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
            machine_count = int(self.machine_count_entry3.get())
            
            # Validate all jobs are assigned
            assigned_jobs = [j for m in self.job_assignments.values() for j in m]
            if len(assigned_jobs) != len(self.unassigned_jobs):
                messagebox.showerror("Error", "Please assign all jobs before calculating")
                return
            
            # Call calculation function with file path and job assignments
            metrics = Parallel_Initial_Calculator(self.selected_file, self.job_assignments, machine_count)
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during calculation: {str(e)}")