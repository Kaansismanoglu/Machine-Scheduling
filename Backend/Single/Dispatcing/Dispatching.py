import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np


def Dispatching_Calculator(file_path, dispatching):
    # Read the data file
    data = pd.read_excel(file_path, engine='openpyxl')
    Job_Number = data['Job Number']
    Processing_Time = data['process time ']
    Due_Date = data['due date ']
    Weight = data['weight']
    Release_Date = data['release date']
    
    if dispatching == "SPT (1| |∑C_j)":
        # Sort jobs based on processing times (SPT rule)
        jobs_with_times = list(zip(Job_Number, Processing_Time))
        jobs_with_times.sort(key=lambda x: x[1])  # Sort by processing time
        
        job_sequence = [job for job, _ in jobs_with_times]
        completion_times = []
        current_time = 0
        
        # Calculate completion time for each job
        for job in job_sequence:
            current_time += Processing_Time[job-1]
            completion_times.append(current_time)
        
        total_completion_time = sum(completion_times)
        
        # Calculate total tardiness, total lateness, and number of tardy jobs
        tardiness = [max(0, completion_times[i] - Due_Date[job_sequence[i]-1]) for i in range(len(job_sequence))]
        total_tardiness = sum(tardiness)
        total_lateness = sum(completion_times[i] - Due_Date[job_sequence[i]-1] for i in range(len(job_sequence)))
        number_of_tardy_jobs = sum(1 for t in tardiness if t > 0)
        
        total_weighted_completion_time = sum(Weight[job-1] * completion_times[i] for i, job in enumerate(job_sequence))
        
        # Prepare data for visualization
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Plot Gantt chart
        current_time = 0
        num_jobs = len(job_sequence)
        colors = cm.get_cmap('tab20', num_jobs)  # Use a colormap with enough distinct colors

        for i, job in enumerate(job_sequence):
            ax.barh(0, Processing_Time[job-1], left=current_time, height=0.3,
                    align='center', color=colors(i), edgecolor='black')
            
            # Add job labels
            ax.text(current_time + Processing_Time[job-1]/2, 0,
                    f'Job {job}', ha='center', va='center')
            
            current_time += Processing_Time[job-1]
        
        # Customize the plot
        ax.set_xlabel('Time')
        ax.set_ylabel('Machine')
        ax.set_title('Single Machine Schedule (Minimize Total Completion Time)')
        ax.set_ylim(-0.5, 0.5)
        ax.set_yticks([0])
        ax.set_yticklabels(['Machine 1'])
        ax.grid(True)
        
        # Add total completion time text
        plt.text(0.02, 0.95, f'Total Completion Time: {total_completion_time}\nTotal Tardiness: {total_tardiness}\nTotal Lateness: {total_lateness}\nNumber of Tardy Jobs: {number_of_tardy_jobs}\nTotal Weighted Completion Time: {total_weighted_completion_time}',
                transform=plt.gca().transAxes,
                bbox=dict(facecolor='white', alpha=0.8))
        
        plt.tight_layout()
        plt.show()
        
        return total_completion_time, job_sequence, total_tardiness, total_lateness, number_of_tardy_jobs
        
    elif dispatching == "LPT (1| |∑C_j)":
        # Sort jobs based on processing times (LPT rule)
        jobs_with_times = list(zip(Job_Number, Processing_Time))
        jobs_with_times.sort(key=lambda x: x[1], reverse=True)  # Sort by processing time in descending order
        
        job_sequence = [job for job, _ in jobs_with_times]
        completion_times = []
        current_time = 0
        
        # Calculate completion time for each job
        for job in job_sequence:
            current_time += Processing_Time[job-1]
            completion_times.append(current_time)
        
        total_completion_time = sum(completion_times)
        
        # Calculate total tardiness, total lateness, and number of tardy jobs
        tardiness = [max(0, completion_times[i] - Due_Date[job_sequence[i]-1]) for i in range(len(job_sequence))]
        total_tardiness = sum(tardiness)
        total_lateness = sum(completion_times[i] - Due_Date[job_sequence[i]-1] for i in range(len(job_sequence)))
        number_of_tardy_jobs = sum(1 for t in tardiness if t > 0)
        
        total_weighted_completion_time = sum(Weight[job-1] * completion_times[i] for i, job in enumerate(job_sequence))
        
        # Prepare data for visualization
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Plot Gantt chart
        current_time = 0
        num_jobs = len(job_sequence)
        colors = cm.get_cmap('tab20', num_jobs)  # Use a colormap with enough distinct colors

        for i, job in enumerate(job_sequence):
            ax.barh(0, Processing_Time[job-1], left=current_time, height=0.3,
                    align='center', color=colors(i), edgecolor='black')
            
            # Add job labels
            ax.text(current_time + Processing_Time[job-1]/2, 0,
                    f'Job {job}', ha='center', va='center')
            
            current_time += Processing_Time[job-1]
        
        # Customize the plot
        ax.set_xlabel('Time')
        ax.set_ylabel('Machine')
        ax.set_title('Single Machine Schedule (LPT Rule)')
        ax.set_ylim(-0.5, 0.5)
        ax.set_yticks([0])
        ax.set_yticklabels(['Machine 1'])
        ax.grid(True)
        
        # Add total completion time text
        plt.text(0.02, 0.95, f'Total Completion Time: {total_completion_time}\nTotal Tardiness: {total_tardiness}\nTotal Lateness: {total_lateness}\nNumber of Tardy Jobs: {number_of_tardy_jobs}\nTotal Weighted Completion Time: {total_weighted_completion_time}',
                transform=plt.gca().transAxes,
                bbox=dict(facecolor='white', alpha=0.8))
        
        plt.tight_layout()
        plt.show()
        
        return total_completion_time, job_sequence, total_tardiness, total_lateness, number_of_tardy_jobs
        
    elif dispatching == "EDD (1| |Lmax)":
        # Sort jobs based on due dates (EDD rule)
        jobs_with_due_dates = list(zip(Job_Number, Due_Date))
        jobs_with_due_dates.sort(key=lambda x: x[1])  # Sort by due date
        
        job_sequence = [job for job, _ in jobs_with_due_dates]
        completion_times = []
        current_time = 0
        
        # Calculate completion time for each job
        for job in job_sequence:
            current_time += Processing_Time[job-1]
            completion_times.append(current_time)
            
        # Calculate maximum lateness
        lateness = [completion_times[i] - Due_Date[job_sequence[i]-1] for i in range(len(job_sequence))]
        max_lateness = max(lateness)
        
        # Calculate total tardiness, total lateness, and number of tardy jobs
        tardiness = [max(0, completion_times[i] - Due_Date[job_sequence[i]-1]) for i in range(len(job_sequence))]
        total_tardiness = sum(tardiness)
        total_lateness = sum(completion_times[i] - Due_Date[job_sequence[i]-1] for i in range(len(job_sequence)))
        number_of_tardy_jobs = sum(1 for t in tardiness if t > 0)
        
        total_weighted_completion_time = sum(Weight[job-1] * completion_times[i] for i, job in enumerate(job_sequence))
        total_completion_time = sum(completion_times)
        
        
        
        # Prepare data for visualization
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Plot Gantt chart
        current_time = 0
        num_jobs = len(job_sequence)
        colors = cm.get_cmap('tab20', num_jobs)  # Use a colormap with enough distinct colors

        for i, job in enumerate(job_sequence):
            ax.barh(0, Processing_Time[job-1], left=current_time, height=0.3,
                    align='center', color=colors(i), edgecolor='black')
            
            # Add job labels with due dates
            ax.text(current_time + Processing_Time[job-1]/2, 0,
                    f'Job {job}\nd={Due_Date[job-1]}', ha='center', va='center')
            
            # Add due date markers with job labels
            ax.axvline(x=Due_Date[job-1], color='red', linestyle='--', alpha=0.3)
            ax.text(Due_Date[job-1], -0.4, f'Due date of Job {job}', rotation=90, ha='right')
            
            current_time += Processing_Time[job-1]
        
        # Customize the plot
        ax.set_xlabel('Time')
        ax.set_ylabel('Machine')
        ax.set_title('Single Machine Schedule (EDD Rule)')
        ax.set_ylim(-0.5, 0.5)
        ax.set_yticks([0])
        ax.set_yticklabels(['Machine 1'])
        ax.grid(True)
        
        # Add maximum lateness text
        plt.text(0.02, 0.95, f'Maximum Lateness: {max_lateness}\nTotal Tardiness: {total_tardiness}\nTotal Lateness: {total_lateness}\nNumber of Tardy Jobs: {number_of_tardy_jobs}\nTotal Weighted Completion Time: {total_weighted_completion_time}\nTotal Completion Time: {total_completion_time}',
                transform=plt.gca().transAxes,
                bbox=dict(facecolor='white', alpha=0.8))
        
        plt.tight_layout()
        plt.show()
        
        return max_lateness, job_sequence, total_tardiness, total_lateness, number_of_tardy_jobs
        
    elif dispatching == "WSPT (1| |∑w_j*C_j)":
        # Calculate weighted processing time ratio for each job
        jobs_with_ratio = [(job, Weight[job-1]/Processing_Time[job-1]) 
                        for job in Job_Number]
        
        # Sort jobs based on weighted shortest processing time (WSPT) rule
        jobs_with_ratio.sort(key=lambda x: x[1], reverse=True)
        
        job_sequence = [job for job, _ in jobs_with_ratio]
        completion_times = []
        current_time = 0
        
        # Calculate completion time and weighted completion time for each job
        weighted_completion_times = []
        for job in job_sequence:
            current_time += Processing_Time[job-1]
            completion_times.append(current_time)
            weighted_completion_times.append(current_time * Weight[job-1])
        
        total_weighted_completion_time = sum(weighted_completion_times)
        total_completion_time = sum(completion_times)
        
        # Calculate total tardiness, total lateness, and number of tardy jobs
        tardiness = [max(0, completion_times[i] - Due_Date[job_sequence[i]-1]) for i in range(len(job_sequence))]
        total_tardiness = sum(tardiness)
        total_lateness = sum(completion_times[i] - Due_Date[job_sequence[i]-1] for i in range(len(job_sequence)))
        number_of_tardy_jobs = sum(1 for t in tardiness if t > 0)
        
        # Prepare data for visualization
        fig, ax = plt.subplots(figsize=(12, 6))
        
        num_jobs = len(job_sequence)
        # Define colors for jobs
        colors = cm.get_cmap('tab20', num_jobs)  # Use a colormap with enough distinct colors
        
        # Plot Gantt chart
        current_time = 0
        for i, job in enumerate(job_sequence):
            ax.barh(0, Processing_Time[job-1], left=current_time, height=0.3,
                    align='center', color=colors(i), edgecolor='black')
            
            # Add job labels with weights
            ax.text(current_time + Processing_Time[job-1]/2, 0,
                    f'Job {job}\nw={Weight[job-1]}', ha='center', va='center')
            
            current_time += Processing_Time[job-1]
        
        # Customize the plot
        ax.set_xlabel('Time')
        ax.set_ylabel('Machine')
        ax.set_title('Single Machine Schedule (WSPT Rule)')
        ax.set_ylim(-0.5, 0.5)
        ax.set_yticks([0])
        ax.set_yticklabels(['Machine 1'])
        ax.grid(True)
        
        # Add total weighted completion time text
        plt.text(0.02, 0.95, f'Total Weighted Completion Time: {total_weighted_completion_time}\nTotal Tardiness: {total_tardiness}\nTotal Lateness: {total_lateness}\nNumber of Tardy Jobs: {number_of_tardy_jobs}\nTotal Completion Time: {total_completion_time}',
                transform=plt.gca().transAxes,
                bbox=dict(facecolor='white', alpha=0.8))
        
        plt.tight_layout()
        plt.show()
        
        return total_weighted_completion_time, job_sequence, total_tardiness, total_lateness, number_of_tardy_jobs
        
    elif dispatching == "SRPT (1|r_j, Pmtn|∑C_j)":
        # Veriyi sıralama ve SRPT algoritması
        jobs = list(zip(Job_Number, Release_Date, Processing_Time))
        jobs.sort(key=lambda x: x[1])  # Release date'e göre sırala

        current_time = 0
        gantt_chart = []
        remaining_jobs = jobs.copy()
        job_times = {job[0]: job[2] for job in jobs}  # Store remaining processing times
        total_completion_time = 0  # Initialize total completion time

        # Initialize tardiness and lateness calculations
        completion_times = []
        tardiness = []
        total_tardiness = 0
        total_lateness = 0
        number_of_tardy_jobs = 0

        # Create a color map for each job
        job_colors = {job[0]: cm.tab20(i) for i, job in enumerate(jobs)}

        while remaining_jobs:
            # Serbest bırakılmış işlerden işlem süresi en kısa olanı seç
            available_jobs = [job for job in remaining_jobs if job[1] <= current_time]
            if available_jobs:
                # İşlem süresi en kısa olan işi seç
                next_job = min(available_jobs, key=lambda x: job_times[x[0]])
                job_number, release_date, process_time = next_job

                # Determine the time slice for processing the current job
                if remaining_jobs and any(job[1] > current_time for job in remaining_jobs):
                    # Find the next job's release time that is greater than the current time
                    next_release_time = min(job[1] for job in remaining_jobs if job[1] > current_time)
                    # Calculate the time slice as the minimum between the remaining process time and the time until the next job is released
                    time_slice = min(process_time, next_release_time - current_time, job_times[job_number])
                    
                else:
                    # If no jobs are remaining or all are available, process the entire remaining time
                    time_slice = job_times[job_number]
                
                gantt_chart.append((current_time, current_time + time_slice, job_number))
                current_time += time_slice
                
                if job_times[job_number] == time_slice:
                    total_completion_time += current_time  # Update total completion time

                # Update remaining processing time
                job_times[job_number] -= time_slice

                # If the job is not finished, keep it in the remaining jobs
                if job_times[job_number] <= 0:  # Job is completed
                    remaining_jobs.remove(next_job)
                    completion_times.append(current_time)
                    tardiness.append(max(0, current_time - Due_Date[job_number - 1]))  # Calculate tardiness
                else:
                    # If the job is not completed, calculate its completion time
                    completion_times.append(current_time)
            else:
                # Check for the next available job's release time
                next_release_time = min(job[1] for job in remaining_jobs)
                current_time = max(current_time, next_release_time)

                # If there are jobs that can be resumed, continue processing
                available_jobs = [job for job in remaining_jobs if job[1] <= current_time]
                if available_jobs:
                    next_job = min(available_jobs, key=lambda x: job_times[x[0]])
                    job_number, release_date, process_time = next_job
                    time_slice = job_times[job_number]
                    gantt_chart.append((current_time, current_time + time_slice, job_number))
                    current_time += time_slice
                    
                    if job_times[job_number] == time_slice:
                        total_completion_time += current_time  # Update total completion time
                    
                    job_times[job_number] = max(0, job_times[job_number] - time_slice)  # Update remaining time correctly
                    if job_times[job_number] == 0:  # Job is completed
                        remaining_jobs.remove(next_job)
                        completion_times.append(current_time)
                        tardiness.append(max(0, current_time - Due_Date[job_number - 1]))  # Calculate tardiness
                else:
                    # If no jobs are available, increment current_time by the remaining time of the next job
                    current_time += min(job[1] for job in remaining_jobs) - current_time  # Update current_time to the next job's release time

        # Calculate total tardiness, total lateness, and number of tardy jobs
        total_tardiness = sum(tardiness)
        total_lateness = sum(completion_times[i] - Due_Date[job_number - 1] for i, job_number in enumerate(Job_Number) if i < len(completion_times))
        number_of_tardy_jobs = sum(1 for t in tardiness if t > 0)
        
        total_weighted_completion_time = sum(Weight[job-1] * completion_times[i] for i, job in enumerate(Job_Number))
        
        

        # Gantt Şeması
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.set_title("Single Machine Schedule (SRPT Rule with Preemption)", fontsize=14, fontweight='bold')
        ax.set_xlabel("Time", fontsize=12)
        ax.set_ylabel("Machine", fontsize=12)
        ax.set_ylim(-0.5, 0.5)
        ax.set_yticks([0])
        ax.set_yticklabels(["Machine 1"], fontsize=12)
        ax.grid(True)

        # Plot Gantt chart with consistent colors for each job
        for start, end, job_number in gantt_chart:
            ax.barh(0, end - start, left=start, height=0.4, align="center", color=job_colors[job_number], edgecolor="black")
            ax.text((start + end) / 2, 0, f"Job {job_number}", ha="center", va="center", color="white", fontsize=10)

        # Add total completion time text to the Gantt chart
        ax.text(0.02, 0.95, f'Total Completion Time: {total_completion_time}\nTotal Tardiness: {total_tardiness}\nTotal Lateness: {total_lateness}\nNumber of Tardy Jobs: {number_of_tardy_jobs}\nTotal Weighted Completion Time: {total_weighted_completion_time}', transform=ax.transAxes,
                bbox=dict(facecolor='white', alpha=0.8))

        # Add release time markers
        for job in jobs:
            ax.axvline(x=job[1], color='red', linestyle='--', alpha=0.5)  # Release time as dashed red line

        # Adjust x-axis limits for better visibility
        ax.set_xlim(0, current_time)  # Set x-axis limit to the current time

        plt.tight_layout()
        plt.show()

        print(f"Total Completion Time: {total_completion_time}")  # Output total completion time
    
    else:
        print("Invalid dispatching rule")
        return None, None
