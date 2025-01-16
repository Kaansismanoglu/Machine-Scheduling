import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np



def calculate_initial_metrics(file_path, sequence):
    # Read the data file
    data = pd.read_excel(file_path, engine='openpyxl')
    Job_Number = data['Job Number']
    Processing_Time = data['process time ']
    Due_Date = data['due date ']
    Weight = data['weight']
    Release_Date = data['release date']
    
    # Initialize variables
    n_jobs = len(sequence)
    current_time = 0
    completion_times = []
    tardiness = []
    weighted_completion_times = []
    
    # Check if release dates and weights are meaningful (not all 0 or 1)
    has_release_dates = not all(x == 0 for x in Release_Date)
    has_weights = not all(x == 1 for x in Weight)
    
    
    # Calculate metrics for each job in sequence
    for job_idx in sequence:
        
        # Get job parameters
        processing_time = Processing_Time[job_idx-1]
        due_date = Due_Date[job_idx-1]
        weight = Weight[job_idx-1]
        release_date = Release_Date[job_idx-1]
        
        print(f'processing_time: {processing_time}, due_date: {due_date}, weight: {weight}, release_date: {release_date}')
        
        # Consider release date if applicable
        if has_release_dates:
            current_time = max(current_time, release_date)
            
        # Calculate completion time
        current_time += processing_time
        completion_times.append(current_time)
        
        # Calculate tardiness
        job_tardiness = max(0, current_time - due_date)
        tardiness.append(job_tardiness)
        
        # Calculate weighted completion time if applicable
        if has_weights:
            weighted_completion_times.append(current_time * weight)
    
    # Calculate summary metrics
    total_completion_time = sum(completion_times)
    max_completion_time = max(completion_times)
    total_tardiness = sum(tardiness)  # Sum of individual job tardiness values
    max_tardiness = max(tardiness)
    total_latency = sum([ct - Due_Date[seq-1] for ct, seq in zip(completion_times, sequence)])  # Sum of completion time minus release date
    num_tardy_jobs = sum(1 for t in tardiness if t > 0)
    
    # Weighted metrics if applicable
    if has_weights:
        total_weighted_completion_time = sum(weighted_completion_times)
    
    # Create color map with unique color for each job
    colors = cm.rainbow(np.linspace(0, 1, len(sequence)))
    
    # Plot Gantt chart
    fig, (ax, text_ax) = plt.subplots(2, 1, figsize=(12, 8), 
                                     gridspec_kw={'height_ratios': [3, 1]})
    
    # Add legend for due date line
    ax.plot([], [], color='red', linestyle='--', label='Due Date', alpha=0.3)
    ax.legend(loc='upper right')
    
    # Plot each job as a horizontal bar with unique color
    current_time = 0
    for i, job in enumerate(sequence):
        # Consider release date if applicable
        if has_release_dates:
            current_time = max(current_time, Release_Date[job-1])
            
        # Plot job bar
        ax.barh(0, Processing_Time[job-1], left=current_time, height=0.3,
                align='center', color=colors[i], edgecolor='black')
        
        # Add job labels with detailed information
        label_text = f'Job {job}\n'
        if has_release_dates:
            label_text += f'r={Release_Date[job-1]}\n'
        if has_weights:
            label_text += f'w={Weight[job-1]}\n'
        label_text += f'd={Due_Date[job-1]}'
        
        ax.text(current_time + Processing_Time[job-1]/2, 0,
                label_text, ha='center', va='center')
        
        # Add due date markers if due dates exist
        if Due_Date[job-1] > 0:
            ax.axvline(x=Due_Date[job-1], color='red', linestyle='--', alpha=0.3)
            # Add job number and due date explanation below due date line
            ax.text(Due_Date[job-1], -0.4, f'Job {job}', 
                   ha='center', va='top', color='red')
        
        current_time += Processing_Time[job-1]
    
    # Customize the Gantt chart
    ax.set_xlabel('Time')
    ax.set_ylabel('Machine')
    ax.set_title('Single Machine Schedule')
    ax.set_ylim(-0.5, 0.5)
    ax.set_yticks([0])
    ax.set_yticklabels(['Machine 1'])
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
        'Individual Tardiness': tardiness
    }
    
    if has_weights:
        metrics.update({
            'Total Weighted Completion Time': total_weighted_completion_time,
            'Individual Weighted Completion Times': weighted_completion_times
        })
    
    return metrics
