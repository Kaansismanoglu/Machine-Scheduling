from base_container import Container
import customtkinter

class SidebarContainer(Container):
    def __init__(self, parent):
        super().__init__(parent, width=140, corner_radius=0)
        
        self.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.grid_rowconfigure(8, weight=1)
        
        # Logo
        self.logo = customtkinter.CTkLabel(self, text="Team 13", 
                                         font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # Navigation buttons
        button_width = 310  # Increased fixed width for all buttons
        
        self.nav_buttons = [
            customtkinter.CTkButton(self, text="Single Machine with Initial Sequence",
                                  command=lambda: parent.sidebar_button_1_event(),
                                  anchor="w", width=button_width),
            customtkinter.CTkButton(self, text="Single Machine with Dispatching Rules", 
                                  command=lambda: parent.sidebar_button_2_event(),
                                  anchor="w", width=button_width),
            customtkinter.CTkButton(self, text="Parallel Machine with Initial Sequence",
                                  command=lambda: parent.sidebar_button_3_event(),
                                  anchor="w", width=button_width),
            customtkinter.CTkButton(self, text="Parallel Machine with Dispatching Rules",
                                  command=lambda: parent.sidebar_button_4_event(),
                                  anchor="w", width=button_width),
            customtkinter.CTkButton(self, text="Flow Shop Scheduling with Johnson's Algorithm",
                                  command=lambda: parent.sidebar_button_5_event(),
                                  anchor="w", width=button_width),
            customtkinter.CTkButton(self, text="Flow Shop Scheduling with Approximation",
                                  command=lambda: parent.sidebar_button_6_event(),
                                  anchor="w", width=button_width),
            customtkinter.CTkButton(self, text="Local Search for Parallel Machine Scheduling",
                                  command=lambda: parent.sidebar_button_7_event(),
                                  anchor="w", width=button_width),
        ]
        
        for i, btn in enumerate(self.nav_buttons, 1):
            btn.grid(row=i, column=0, padx=20, pady=10, sticky="w")
            
        # Appearance controls
        self.appearance_label = customtkinter.CTkLabel(self, text="Appearance Mode:", anchor="w")
        self.appearance_label.grid(row=9, column=0, padx=20, pady=(10, 0))
        
        self.appearance_menu = customtkinter.CTkOptionMenu(self, values=["Light", "Dark", "System"],
                                                         command=parent.change_appearance_mode_event,
                                                         width=button_width)  # Added fixed width
        self.appearance_menu.grid(row=10, column=0, padx=20, pady=(10, 10))
        
        self.scaling_label = customtkinter.CTkLabel(self, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=11, column=0, padx=20, pady=(10, 0))
        
        self.scaling_menu = customtkinter.CTkOptionMenu(self, values=["80%", "90%", "100%", "110%", "120%"],
                                                      command=parent.change_scaling_event,
                                                      width=button_width)  # Added fixed width
        self.scaling_menu.grid(row=12, column=0, padx=20, pady=(10, 20))