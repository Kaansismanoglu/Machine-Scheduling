import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def Flow_Shop_Algorithms(file_path):
    # Read the data file
    data = pd.read_excel(file_path, engine='openpyxl')
    Job_Number = data['Job Number']
    Processing_Times = data[['Processing Time for Machine 1', 'Processing Time for Machine 2']]
    weights = data['weight']
    Due_date = data['due date ']
    
    machine1_jobs = []
    machine2_jobs = []

    # Check if the number of machines is valid
    num_machines = 2
    
    # Compare Processing Time for Machine 1 and Machine 2
    for i in range(len(Processing_Times)):
        if Processing_Times['Processing Time for Machine 1'][i] >= Processing_Times['Processing Time for Machine 2'][i]:
            machine2_jobs.append(Job_Number[i])
        else:
            machine1_jobs.append(Job_Number[i])

    # Sorting SPT for Machine 1
    machine1_jobs.sort(key=lambda x: Processing_Times['Processing Time for Machine 1'][Job_Number[x-1]-1])
    
    # Sorting LPT for Machine 2
    machine2_jobs.sort(key=lambda x: Processing_Times['Processing Time for Machine 2'][Job_Number[x-1]-1], reverse=True)
    
    # Schedule job list
    schedule = machine1_jobs + machine2_jobs
    
    print("Job Sequence: ", schedule)
    
    # Initialize makespan, total completion time, total tardiness, and total weighted tardiness
    makespan = 0
    total_completion_time = 0
    total_weighted_completion_time = 0
    total_tardiness = 0  # Initialize total tardiness
    total_weighted_tardiness = 0  # Initialize total weighted tardiness
    
    # Showing on Gantt Chart
    fig, gnt = plt.subplots()
    gnt.set_title('Flow Shop Chart')
    gnt.set_xlabel('Time')
    gnt.set_ylabel('Jobs')
    # Create a color map for the Gantt chart with unique colors for each job
    colors = plt.cm.get_cmap('tab20', len(schedule))  # Generate a colormap with better color representation
    start_time_machine1 = 0
    start_time_machine2 = 0
    
    for i in range(len(schedule)):
        job_name = Job_Number[schedule[i]-1]  # Get the job name
        processing_time_machine1 = Processing_Times['Processing Time for Machine 1'][schedule[i]-1]
        processing_time_machine2 = Processing_Times['Processing Time for Machine 2'][schedule[i]-1]
        
        gnt.broken_barh([(start_time_machine1, processing_time_machine1)], (10, 9), facecolors=colors(i))
        gnt.text(start_time_machine1 + processing_time_machine1 / 2, 15, f"Job {str(job_name)}", ha='center', va='center')  # Add job name for Machine 1
        start_time_machine1 += processing_time_machine1
        
        start_time_machine2 = max(start_time_machine1, start_time_machine2)  # Machine 2 can start when Machine 1 is done
        gnt.broken_barh([(start_time_machine2, processing_time_machine2)], (20, 9), facecolors=colors(i))
        gnt.text(start_time_machine2 + processing_time_machine2 / 2, 25, f"Job {str(job_name)}", ha='center', va='center')  # Add job name for Machine 2
        start_time_machine2 += processing_time_machine2
        
        total_completion_time = total_completion_time + start_time_machine2  # The total completion time is the time when all jobs are done
        
        total_weighted_completion_time = total_weighted_completion_time + (start_time_machine2 * weights[schedule[i]-1])  # Calculate the total weighted completion time
        
        # Calculate tardiness for the job
        tardiness = max(0, start_time_machine2 - Due_date[schedule[i]-1])  # Calculate tardiness for the job
        total_tardiness += tardiness  # Accumulate total tardiness
        
        # Calculate weighted tardiness for the job
        weighted_tardiness = tardiness * weights[schedule[i]-1]  # Calculate weighted tardiness
        total_weighted_tardiness += weighted_tardiness  # Accumulate total weighted tardiness
        
    gnt.set_yticks([15, 25])
    gnt.set_yticklabels(['Machine 1', 'Machine 2'])
    
    # Calculate makespan and total completion time
    makespan = start_time_machine2  # The makespan is the total time taken for all jobs
    print("Makespan: ", makespan)
    print("Total Completion Time: ", total_completion_time)
    print("Total Weighted Completion Time: ", total_weighted_completion_time)
    print("Total Tardiness: ", total_tardiness)  # Print total tardiness
    print("Total Weighted Tardiness: ", total_weighted_tardiness)  # Print total weighted tardiness

    # Display makespan, total completion time, total tardiness, and total weighted tardiness on the Gantt chart at the top left corner
    gnt.text(0, 32, f"Makespan: {makespan}", ha='left', va='center', fontsize=9, color='red', fontweight='bold')
    gnt.text(0, 31.5, f"Total Completion Time: {total_completion_time}", ha='left', va='center', fontsize=9, color='blue', fontweight='bold')
    gnt.text(0, 31, f"Total Weighted Completion Time: {total_weighted_completion_time}", ha='left', va='center', fontsize=9, color='green', fontweight='bold')
    gnt.text(0, 30.5, f"Total Tardiness: {total_tardiness}", ha='left', va='center', fontsize=9, color='orange', fontweight='bold')  # Display total tardiness
    gnt.text(0, 30, f"Total Weighted Tardiness: {total_weighted_tardiness}", ha='left', va='center', fontsize=9, color='purple', fontweight='bold')  # Display total weighted tardiness

    plt.show()
