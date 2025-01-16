import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

def Parallel_Initial_Calculator(file_path, job_assignments, num_machines):
    # Read the data file
    data = pd.read_excel(file_path, engine='openpyxl')
    Job_Number = data['Job Number']
    Processing_Time = data['process time ']
    Due_Date = data['due date ']
    Weight = data['weight']
    Release_Date = data['release date']
    
    # Initialize variables
    machine_times = [0] * num_machines  # Track time for each machine
    completion_times = []
    tardiness = []
    weighted_completion_times = []
    job_machine_assignments = []  # Track which job is assigned to which machine
    
    # Check if release dates and weights are meaningful (not all 0 or 1)
    has_release_dates = not all(x == 0 for x in Release_Date)
    has_weights = not all(x == 1 for x in Weight)
    
    # Sort jobs by release date for each machine
    for machine in range(1, num_machines + 1):
        if machine not in job_assignments:
            continue
        
        current_time = 0  # Start time for this machine
        
        for job_idx in job_assignments[machine]:
            # Get job parameters from data file
            processing_time = Processing_Time[job_idx-1]
            due_date = Due_Date[job_idx-1]
            weight = Weight[job_idx-1]
            release_date = Release_Date[job_idx-1]
            
            # Consider release date if applicable
            if has_release_dates:
                current_time = max(current_time, release_date)
                
            # Calculate completion time
            completion_time = current_time + processing_time
            current_time = completion_time  # Update current time for next job
            completion_times.append(completion_time)
            job_machine_assignments.append((job_idx, machine-1))
            
            # Calculate tardiness
            job_tardiness = max(0, completion_time - due_date)
            tardiness.append(job_tardiness)
            
            # Calculate weighted completion time if applicable
            if has_weights:
                weighted_completion_times.append(completion_time * weight)
            
        machine_times[machine-1] = current_time  # Store final time for this machine
    
    # Calculate summary metrics
    total_completion_time = sum(completion_times)
    max_completion_time = max(completion_times)
    total_tardiness = sum(tardiness)
    max_tardiness = max(tardiness)
    
    # Get all jobs in sequence
    sequence = []
    for machine in range(1, num_machines + 1):
        if machine in job_assignments:
            sequence.extend(job_assignments[machine])
            
    total_latency = sum([ct - Due_Date[seq-1] for ct, seq in zip(completion_times, sequence)])
    num_tardy_jobs = sum(1 for t in tardiness if t > 0)
    
    # Weighted metrics if applicable
    if has_weights:
        total_weighted_completion_time = sum(weighted_completion_times)
    
    # Create color map with unique color for each job
    colors = cm.rainbow(np.linspace(0, 1, len(sequence)))
    
    # Plot Gantt chart
    fig, (ax, text_ax) = plt.subplots(2, 1, figsize=(12, 8),
                                     gridspec_kw={'height_ratios': [3, 1]})
    
    # Add legend for due date and release date lines
    ax.plot([], [], color='red', linestyle='--', label='Due Date', alpha=0.3)
    ax.plot([], [], color='blue', linestyle='--', label='Release Date', alpha=0.3)
    ax.legend(loc='upper right')
    
    # Plot each job as a horizontal bar with unique color
    for i, (job, machine) in enumerate(job_machine_assignments):
        # Get start time based on release date and previous job completion
        if i == 0 or job_machine_assignments[i-1][1] != machine:
            # First job on machine - use release date
            start_time = Release_Date[job-1]
        else:
            # Not first job - use max of release date and previous completion time
            start_time = max(Release_Date[job-1], completion_times[i-1])
            
        # Plot job bar
        ax.barh(machine, Processing_Time[job-1], left=start_time, height=0.3,
                align='center', color=colors[i], edgecolor='black')
        
        # Add job labels with detailed information
        label_text = f'Job {job}\n'
        if has_release_dates:
            label_text += f'r={Release_Date[job-1]}\n'
        if has_weights:
            label_text += f'w={Weight[job-1]}\n'
        label_text += f'd={Due_Date[job-1]}'
        
        ax.text(start_time + Processing_Time[job-1]/2, machine,
                label_text, ha='center', va='center')
        
        # Add due date markers if due dates exist
        if Due_Date[job-1] > 0:
            ax.axvline(x=Due_Date[job-1], color='red', linestyle='--', alpha=0.3)
            # Add job number and due date explanation below due date line
            ax.text(Due_Date[job-1], -0.4, f'Job {job} due', 
                   ha='center', va='top', color='red')
                   
        # Add release date markers if release dates exist
        if has_release_dates and Release_Date[job-1] > 0:
            ax.axvline(x=Release_Date[job-1], color='blue', linestyle='--', alpha=0.3)
            # Add job number and release date explanation below release date line
            ax.text(Release_Date[job-1], -0.2, f'Job {job} release', 
                   ha='center', va='top', color='blue')
    
    # Customize the Gantt chart
    ax.set_xlabel('Time')
    ax.set_ylabel('Machines')
    ax.set_title('Parallel Machine Schedule')
    ax.set_ylim(-0.5, num_machines-0.5)
    ax.set_yticks(range(num_machines))
    ax.set_yticklabels([f'Machine {i+1}' for i in range(num_machines)])
    ax.grid(True)
    
    # Add metrics text to bottom subplot
    metrics_text = (
        f'Total Completion Time: {total_completion_time:.2f}\n'
        f'Maximum Completion Time: {max_completion_time:.2f}\n'
        f'Total Tardiness: {total_tardiness:.2f}\n'
        f'Maximum Tardiness: {max_tardiness:.2f}\n'
        f'Total Latency: {total_latency:.2f}\n'
        f'Number of Tardy Jobs: {num_tardy_jobs}\n'
    )
    
    if has_weights:
        metrics_text += (
            f'Total Weighted Completion Time: {total_weighted_completion_time:.2f}\n'
        )
    
    text_ax.text(0.05, 0.5, metrics_text,
                 va='center', fontsize=10,
                 bbox=dict(facecolor='white', alpha=0.8))
    text_ax.axis('off')
    
    plt.tight_layout()
    plt.show()
    
    metrics = {
        'Total Completion Time': total_completion_time,
        'Maximum Completion Time': max_completion_time,
        'Total Tardiness': total_tardiness,
        'Maximum Tardiness': max_tardiness,
        'Total Latency': total_latency,
        'Number of Tardy Jobs': num_tardy_jobs,
        'Individual Completion Times': completion_times,
        'Individual Tardiness': tardiness,
        'Job Machine Assignments': job_machine_assignments
    }
    
    if has_weights:
        metrics.update({
            'Total Weighted Completion Time': total_weighted_completion_time,
            'Individual Weighted Completion Times': weighted_completion_times
        })
    
    return metrics
