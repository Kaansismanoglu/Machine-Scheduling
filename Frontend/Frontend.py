import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter
import tkinter.messagebox
import customtkinter

# Containers
from Sidebar.Sidebar import SidebarContainer
from Single_Machine_Container.tabcontainer_Single_Machine_Dispatching import TabContainer as TabContainer_Dispatching
from Single_Machine_Container.tabcontainer_Single_Machine_Initial_Sequence import TabContainer_Initial_Sequence
from Parallel_Machine_Container.Parallel_Tab_Initial import TabContainer_Parallel_Initial
from Parallel_Machine_Container.Parallel_Tab_Dispatching import TabContainer_Parallel_Dispatching
from Flow_Shop_Container.Approximation.tabcontainer_Approximation import FlowShop_Approximation_Container
from Flow_Shop_Container.Dispatching.tabcontainer_flowshop import FlowShop_Container
from Local_Search_Flow_Shop.Local_Search_Flow_Shop_Container import TabContainer_Local_Search_Flow_Shop

# Set appearance mode and default color
customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

#Main Application
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Window configuration
        self.title("Machine Scheduling")
        self.geometry(f"{1200}x{680}")
        
        # Grid configuration
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2), weight=2)
        self.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)

        # Initialize containers
        self.sidebar = SidebarContainer(self)
        self.tab_container_dispatching = TabContainer_Dispatching(self)
        self.tab_container_initial_sequence = TabContainer_Initial_Sequence(self)
        self.tab_container_parallel_initial = TabContainer_Parallel_Initial(self)
        self.tab_container_parallel_dispatching = TabContainer_Parallel_Dispatching(self)
        self.tab_container_flowshop = FlowShop_Container(self)
        self.tab_container_Approximation = FlowShop_Approximation_Container(self)
        self.tab_container_local_search = TabContainer_Local_Search_Flow_Shop(self)

        # Set default values
        self.sidebar.appearance_menu.set("Dark")
        self.sidebar.scaling_menu.set("100%")
        self.tab_container_dispatching.gamma_menu.set("Please Select Objective Function")
        self.tab_container_parallel_dispatching.rule_menu.set("Please Select Dispatching Rule")
        self.tab_container_flowshop.gamma_menu5.set("Johnson's Algorithm")
        self.tab_container_Approximation.gamma_menu6.set("Please Select Approximation Algorithm")
        self.tab_container_local_search.rule_menu7.set("Please Select Objective Function")

        # Initially hide components
        self.tab_container_dispatching.grid_remove()
        self.tab_container_dispatching.main_button.grid_remove()
        self.tab_container_parallel_initial.grid_remove()
        self.tab_container_parallel_initial.main_button3.grid_remove()
        self.tab_container_parallel_dispatching.grid_remove()
        self.tab_container_parallel_dispatching.main_button4.grid_remove()
        self.tab_container_flowshop.grid_remove()
        self.tab_container_flowshop.main_button5.grid_remove()
        self.tab_container_Approximation.grid_remove()
        self.tab_container_Approximation.main_button6.grid_remove()
        self.tab_container_local_search.grid_remove()
        self.tab_container_local_search.main_button7.grid_remove()
        
        
    # Appearance Mode
    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
        
        
    # Sidebar Functions
    def sidebar_button_1_event(self):
        self.tab_container_initial_sequence.grid()
        self.tab_container_initial_sequence.main_button.grid()
        
        self.tab_container_dispatching.grid_remove()
        self.tab_container_dispatching.main_button.grid_remove()
        
        self.tab_container_parallel_initial.grid_remove()
        self.tab_container_parallel_initial.main_button3.grid_remove()
        
        self.tab_container_parallel_dispatching.grid_remove()
        self.tab_container_parallel_dispatching.main_button4.grid_remove()
        
        self.tab_container_flowshop.grid_remove()
        self.tab_container_flowshop.main_button5.grid_remove()
        
        self.tab_container_Approximation.grid_remove()
        self.tab_container_Approximation.main_button6.grid_remove()
        
        self.tab_container_local_search.grid_remove()
        self.tab_container_local_search.main_button7.grid_remove()
    
    def sidebar_button_2_event(self):
        self.tab_container_dispatching.grid()
        self.tab_container_dispatching.main_button.grid()
        
        self.tab_container_initial_sequence.grid_remove()
        self.tab_container_initial_sequence.main_button.grid_remove()
        
        self.tab_container_parallel_initial.grid_remove()
        self.tab_container_parallel_initial.main_button3.grid_remove()
        
        self.tab_container_parallel_dispatching.grid_remove()
        self.tab_container_parallel_dispatching.main_button4.grid_remove()
        
        self.tab_container_flowshop.grid_remove()
        self.tab_container_flowshop.main_button5.grid_remove()
        
        self.tab_container_Approximation.grid_remove()
        self.tab_container_Approximation.main_button6.grid_remove()
        
        self.tab_container_local_search.grid_remove()
        self.tab_container_local_search.main_button7.grid_remove()
        
    def sidebar_button_3_event(self):
        self.tab_container_parallel_initial.grid()
        self.tab_container_parallel_initial.main_button3.grid()
        
        self.tab_container_initial_sequence.grid_remove()
        self.tab_container_initial_sequence.main_button.grid_remove()
        
        self.tab_container_dispatching.grid_remove()
        self.tab_container_dispatching.main_button.grid_remove()
        
        self.tab_container_parallel_dispatching.grid_remove()
        self.tab_container_parallel_dispatching.main_button4.grid_remove()
        
        self.tab_container_flowshop.grid_remove()
        self.tab_container_flowshop.main_button5.grid_remove()
        
        self.tab_container_Approximation.grid_remove()
        self.tab_container_Approximation.main_button6.grid_remove()
        
        self.tab_container_local_search.grid_remove()
        self.tab_container_local_search.main_button7.grid_remove()
        
    def sidebar_button_4_event(self):
        self.tab_container_parallel_dispatching.grid()
        self.tab_container_parallel_dispatching.main_button4.grid()
        
        self.tab_container_parallel_initial.grid_remove()
        self.tab_container_parallel_initial.main_button3.grid_remove()
        
        self.tab_container_dispatching.grid_remove()
        self.tab_container_dispatching.main_button.grid_remove()
        
        self.tab_container_initial_sequence.grid_remove()
        self.tab_container_initial_sequence.main_button.grid_remove()
        
        self.tab_container_flowshop.grid_remove()
        self.tab_container_flowshop.main_button5.grid_remove()
        
        self.tab_container_local_search.grid_remove()
        self.tab_container_local_search.main_button7.grid_remove()
        
    def sidebar_button_5_event(self):
        self.tab_container_flowshop.grid()
        self.tab_container_flowshop.main_button5.grid()
        
        self.tab_container_parallel_dispatching.grid_remove()
        self.tab_container_parallel_dispatching.main_button4.grid_remove()
        
        self.tab_container_parallel_initial.grid_remove()
        self.tab_container_parallel_initial.main_button3.grid_remove()
        
        self.tab_container_dispatching.grid_remove()
        self.tab_container_dispatching.main_button.grid_remove()
        
        self.tab_container_initial_sequence.grid_remove()
        self.tab_container_initial_sequence.main_button.grid_remove()
        
        self.tab_container_Approximation.grid_remove()
        self.tab_container_Approximation.main_button6.grid_remove()
        
        self.tab_container_local_search.grid_remove()
        self.tab_container_local_search.main_button7.grid_remove()
        
    def sidebar_button_6_event(self):
        self.tab_container_Approximation.grid()
        self.tab_container_Approximation.main_button6.grid()
        
        self.tab_container_parallel_dispatching.grid_remove()
        self.tab_container_parallel_dispatching.main_button4.grid_remove()
        
        self.tab_container_parallel_initial.grid_remove()
        self.tab_container_parallel_initial.main_button3.grid_remove()
        
        self.tab_container_dispatching.grid_remove()
        self.tab_container_dispatching.main_button.grid_remove()
        
        self.tab_container_initial_sequence.grid_remove()
        self.tab_container_initial_sequence.main_button.grid_remove()
        
        self.tab_container_flowshop.grid_remove()
        self.tab_container_flowshop.main_button5.grid_remove()
        
        self.tab_container_local_search.grid_remove()
        self.tab_container_local_search.main_button7.grid_remove()
        
    def sidebar_button_7_event(self):
        self.tab_container_local_search.grid()
        self.tab_container_local_search.main_button7.grid()
        
        self.tab_container_Approximation.grid_remove()
        self.tab_container_Approximation.main_button6.grid_remove()
        
        self.tab_container_parallel_dispatching.grid_remove()
        self.tab_container_parallel_dispatching.main_button4.grid_remove()
        
        self.tab_container_parallel_initial.grid_remove()
        self.tab_container_parallel_initial.main_button3.grid_remove()
        
        self.tab_container_dispatching.grid_remove()
        self.tab_container_dispatching.main_button.grid_remove()
        
        self.tab_container_initial_sequence.grid_remove()
        self.tab_container_initial_sequence.main_button.grid_remove()
        
        self.tab_container_flowshop.grid_remove()
        self.tab_container_flowshop.main_button5.grid_remove()
        

if __name__ == "__main__":
    app = App()
    app.mainloop()