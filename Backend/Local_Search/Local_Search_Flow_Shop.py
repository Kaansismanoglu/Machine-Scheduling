import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np


from Backend.Local_Search.Adjacent.Makespan import Makespan_Adjacent
from Backend.Local_Search.Adjacent.TotalCompletionTime import Total_Completion_Time_Adjacent
from Backend.Local_Search.Adjacent.Total_Weighted_Completin_Time import Total_Weighted_Completion_Time_Adjacent
from Backend.Local_Search.Adjacent.Total_Tardiness import Total_Tardiness_Adjacent
from Backend.Local_Search.Adjacent.Total_Weighted_Tardiness import Total_Weighted_Tardiness_Adjacent
from Backend.Local_Search.Adjacent.Maximum_Tardiness import Maximum_Tardiness_Adjacent
from Backend.Local_Search.Adjacent.Number_of_Tardy_Jobs import Number_of_Tardy_Jobs_Adjacent



# from Adjacent.Makespan import Makespan_Adjacent
# from Adjacent.TotalCompletionTime import Total_Completion_Time_Adjacent
# from Adjacent.Total_Weighted_Completin_Time import Total_Weighted_Completion_Time_Adjacent
# from Adjacent.Total_Tardiness import Total_Tardiness_Adjacent
# from Adjacent.Total_Weighted_Tardiness import Total_Weighted_Tardiness_Adjacent
# from Adjacent.Maximum_Tardiness import Maximum_Tardiness_Adjacent
# from Adjacent.Number_of_Tardy_Jobs import Number_of_Tardy_Jobs_Adjacent

def Local_Search_Calculator(objective, file_path, job_assignments, num_machines, iterations, runtime):

    # Read the data file
    data = pd.read_excel(file_path, engine='openpyxl')
    Job_Number = data['Job Number']
    Processing_Times = data[[f'Processing Time for Machine {i}' for i in range(1, num_machines+1)]]
    Weights = data['weight']
    Due_Date = data['due date ']
    
    
    # Initialize the job sequence
    job_sequence = []
    for key in job_assignments:
        job_sequence += job_assignments[key]

    if objective == "Makespan":
        Makespan_Adjacent(Processing_Times, job_sequence, num_machines, iterations, runtime)
        
    elif objective == "Total Completion Time":
        Total_Completion_Time_Adjacent(Processing_Times, job_sequence, num_machines, iterations, runtime)
        
    elif objective == "Total Weighted Completion Time":
        Total_Weighted_Completion_Time_Adjacent(Processing_Times, job_sequence, Weights, num_machines, iterations, runtime)
    
    elif objective == "Total Tardiness":
        Total_Tardiness_Adjacent(Processing_Times, job_sequence, Due_Date, num_machines, iterations, runtime)
    
    elif objective == "Total Weighted Tardiness":
        Total_Weighted_Tardiness_Adjacent(Processing_Times, job_sequence, Due_Date, Weights, num_machines, iterations, runtime)
        
    elif objective == "Maximum Tardiness":
        Maximum_Tardiness_Adjacent(Processing_Times, job_sequence, Due_Date, num_machines, iterations, runtime)
        
    elif objective == "Number of Tardy Jobs":
        Number_of_Tardy_Jobs_Adjacent(Processing_Times, job_sequence, Due_Date, num_machines, iterations, runtime)
    else:
        print("Invalid objective function")
        
        
    
        

