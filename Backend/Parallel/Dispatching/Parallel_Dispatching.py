import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

def Parallel_Dispacthing_Calculator(file_path, num_machines, selected_rule):
    # Read the data file
    data = pd.read_excel(file_path, engine='openpyxl')
    Job_Number = data['Job Number']
    Processing_Time = data['process time ']
    Due_Date = data['due date ']
    Weight = data['weight']
    Release_Date = data['release date']
    
    if selected_rule == "LPT":
        # Sort jobs based on processing times (LPT rule - Longest Processing Time first)
        jobs_with_times = list(zip(Job_Number, Processing_Time, Weight))
        jobs_with_times.sort(key=lambda x: x[1], reverse=True)  # Sort by processing time in descending order
        
        job_sequence = [job for job, _, _ in jobs_with_times]
        machine_schedules = [[] for _ in range(num_machines)]
        machine_times = [0] * num_machines
        
        total_completion_time = 0  # Initialize total completion time
        total_weighted_completion_time = 0
        total_tardiness = 0  # Initialize total tardiness
        total_lateness = 0  # Initialize total lateness
        total_tardy_jobs = 0  # Initialize total number of tardy jobs
        
        # Assign jobs to machines
        for job, _, weight in jobs_with_times:
            # Find machine with minimum current time
            min_time_machine = machine_times.index(min(machine_times))
            machine_schedules[min_time_machine].append(job)
            machine_times[min_time_machine] += Processing_Time[job-1]
            total_completion_time += machine_times[min_time_machine]  # Update total completion time
            total_weighted_completion_time += machine_times[min_time_machine] * weight 
        
            # Calculate tardiness and lateness for the current job
            due_date = Due_Date[job-1]
            job_tardiness = max(0, machine_times[min_time_machine] - due_date)
            total_tardiness += job_tardiness  # Update total tardiness
            total_tardy_jobs += 1 if job_tardiness > 0 else 0  # Count tardy job
            job_lateness = machine_times[min_time_machine] - due_date
            total_lateness += job_lateness  # Update total lateness
        
        makespan = max(machine_times)
        
        # Prepare data for visualization
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Plot Gantt chart
        colors = cm.get_cmap('tab20', len(job_sequence))
        
        for machine_id, schedule in enumerate(machine_schedules):
            current_time = 0
            for job in schedule:
                ax.barh(machine_id, Processing_Time[job-1], left=current_time, 
                       height=0.3, align='center', 
                       color=colors(job-1), edgecolor='black')
                
                # Add job labels
                ax.text(current_time + Processing_Time[job-1]/2, machine_id,
                       f'Job {job}\nDue: {Due_Date[job-1]}', ha='center', va='center')
                
                # Draw due date line
                ax.axvline(x=Due_Date[job-1], color='red', linestyle='--', linewidth=1)
                # Add job number below the due date line
                ax.text(Due_Date[job-1], machine_id - 0.2, f'Job {job}', ha='center', va='top', color='red')
                
                current_time += Processing_Time[job-1]
        
        # Customize the plot
        ax.set_xlabel('Time')
        ax.set_ylabel('Machines')
        ax.set_title('Parallel Machine Schedule (LPT Rule)')
        ax.set_ylim(-0.5, num_machines-0.5)
        ax.set_yticks(range(num_machines))
        ax.set_yticklabels([f'Machine {i+1}' for i in range(num_machines)])
        ax.grid(True)
        
        # Add makespan, total completion time, total weighted completion time, total tardiness, total lateness, and total tardy jobs text
        plt.text(0.02, 0.95, f'Makespan: {makespan}',
                transform=plt.gca().transAxes,
                bbox=dict(facecolor='white', alpha=0.8))
        plt.text(0.02, 0.90, f'Total Completion Time: {total_completion_time}',
                transform=plt.gca().transAxes,
                bbox=dict(facecolor='white', alpha=0.8))
        plt.text(0.3, 0.95, f'Total Weighted Completion Time: {total_weighted_completion_time}',
                transform=plt.gca().transAxes,
                bbox=dict(facecolor='white', alpha=0.8))
        plt.text(0.3, 0.90, f'Total Tardiness: {total_tardiness}',
                transform=plt.gca().transAxes,
                bbox=dict(facecolor='white', alpha=0.8))
        plt.text(0.6, 0.95, f'Total Lateness: {total_lateness}',
                transform=plt.gca().transAxes,
                bbox=dict(facecolor='white', alpha=0.8))
        plt.text(0.6, 0.90, f'Number of Tardy Jobs: {total_tardy_jobs}',
                transform=plt.gca().transAxes,
                bbox=dict(facecolor='white', alpha=0.8))
        
        plt.tight_layout()
        plt.show()
        
    elif selected_rule == "SPT":
        # Sort jobs by processing time (shortest first)
        jobs_with_times = [(i+1, Processing_Time[i], Weight[i]) for i in range(len(Processing_Time))]
        jobs_with_times.sort(key=lambda x: x[1])  # Sort by processing time
        
        job_sequence = [job for job, _, _ in jobs_with_times]
        machine_schedules = [[] for _ in range(num_machines)]
        machine_times = [0] * num_machines
        
        total_completion_time = 0  # Initialize total completion time
        total_weighted_completion_time = 0
        total_tardiness = 0  # Initialize total tardiness
        total_lateness = 0  # Initialize total lateness
        total_tardy_jobs = 0  # Initialize total number of tardy jobs
        
        # Assign jobs to machines
        for job, _, weight in jobs_with_times:
            # Find machine with minimum current time
            min_time_machine = machine_times.index(min(machine_times))
            machine_schedules[min_time_machine].append(job)
            machine_times[min_time_machine] += Processing_Time[job-1]
            total_completion_time += machine_times[min_time_machine]  # Update total completion time
            total_weighted_completion_time += machine_times[min_time_machine] * weight 
        
            # Calculate tardiness and lateness for the current job
            due_date = Due_Date[job-1]
            job_tardiness = max(0, machine_times[min_time_machine] - due_date)
            total_tardiness += job_tardiness  # Update total tardiness
            total_tardy_jobs += 1 if job_tardiness > 0 else 0  # Count tardy job
            job_lateness = machine_times[min_time_machine] - due_date
            total_lateness += job_lateness  # Update total lateness
        
        makespan = max(machine_times)
        
        # Prepare data for visualization
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Plot Gantt chart
        colors = cm.get_cmap('tab20', len(job_sequence))
        
        for machine_id, schedule in enumerate(machine_schedules):
            current_time = 0
            for job in schedule:
                ax.barh(machine_id, Processing_Time[job-1], left=current_time, 
                       height=0.3, align='center', 
                       color=colors(job-1), edgecolor='black')
                
                # Add job labels
                ax.text(current_time + Processing_Time[job-1]/2, machine_id,
                       f'Job {job}\nDue: {Due_Date[job-1]}', ha='center', va='center')
                
                # Draw due date line
                ax.axvline(x=Due_Date[job-1], color='red', linestyle='--', linewidth=1)
                # Add job number below the due date line
                ax.text(Due_Date[job-1], machine_id - 0.2, f'Job {job}', ha='center', va='top', color='red')
                
                current_time += Processing_Time[job-1]
        
        # Customize the plot
        ax.set_xlabel('Time')
        ax.set_ylabel('Machines')
        ax.set_title('Parallel Machine Schedule (SPT Rule)')
        ax.set_ylim(-0.5, num_machines-0.5)
        ax.set_yticks(range(num_machines))
        ax.set_yticklabels([f'Machine {i+1}' for i in range(num_machines)])
        ax.grid(True)
        
        # Add makespan, total completion time, total weighted completion time, total tardiness, total lateness, and total tardy jobs text
        plt.text(0.02, 0.95, f'Makespan: {makespan}',
                transform=plt.gca().transAxes,
                bbox=dict(facecolor='white', alpha=0.8))
        plt.text(0.02, 0.90, f'Total Completion Time: {total_completion_time}',
                transform=plt.gca().transAxes,
                bbox=dict(facecolor='white', alpha=0.8))
        plt.text(0.3, 0.95, f'Total Weighted Completion Time: {total_weighted_completion_time}',
                transform=plt.gca().transAxes,
                bbox=dict(facecolor='white', alpha=0.8))
        plt.text(0.3, 0.90, f'Total Tardiness: {total_tardiness}',
                transform=plt.gca().transAxes,
                bbox=dict(facecolor='white', alpha=0.8))
        plt.text(0.6, 0.95, f'Total Lateness: {total_lateness}',
                transform=plt.gca().transAxes,
                bbox=dict(facecolor='white', alpha=0.8))
        plt.text(0.6, 0.90, f'Number of Tardy Jobs: {total_tardy_jobs}',
                transform=plt.gca().transAxes,
                bbox=dict(facecolor='white', alpha=0.8))
        
        plt.tight_layout()
        plt.show()
        
    elif selected_rule == "Wrap-Around":
        # 1. Tüm işleri bir tek makinede sırala
        single_machine_schedule = []
        current_time = 0

        for job, processing_time in zip(Job_Number, Processing_Time):
            single_machine_schedule.append((job, current_time, processing_time))
            current_time += processing_time

        print("Single Machine Schedule:", single_machine_schedule)

        # 2. Cutting Point hesapla
        total_processing_time = sum(Processing_Time)
        print("Total Processing Time:", total_processing_time)

        cutting_point = total_processing_time / num_machines
        print("Cutting Point:", cutting_point)
        
        if cutting_point < max(Processing_Time):
            cutting_point = max(Processing_Time)
        

        # 3. Preemption ve İşleri Makinelere Atama
        machine_schedules = [[] for _ in range(num_machines)]
        current_times = [0] * num_machines  # Her makinenin başlangıç zamanı sıfır
        job_remaining_times = Processing_Time[:]  # İşlerin kalan süreleri

        # İşleri makinelerde sırasıyla işlemeye başla
        machine_idx = 0  # İlk makine ile başla
        for job_idx, processing_time in enumerate(Processing_Time):
            remaining_time = processing_time  # İşin başlangıç süresi
            while remaining_time > 0:
                # Eğer mevcut makine cutting point'e kadar işlerse, devam et
                time_to_cut = cutting_point - current_times[machine_idx]
                if time_to_cut > 0:  # Cutting point'e kadar kalan süre
                    time_to_process = min(remaining_time, time_to_cut)  # İşin işlenmesi
                    machine_schedules[machine_idx].append((Job_Number[job_idx], current_times[machine_idx], time_to_process))
                    current_times[machine_idx] += time_to_process
                    remaining_time -= time_to_process
                # Eğer cutting point'ten sonrasına geçilirse, diğer makinede devam et
                if remaining_time > 0:
                    machine_idx = (machine_idx + 1) % num_machines  # Bir sonraki makineye geç
                    current_times[machine_idx] = 0  # Diğer makinelerde başlama zamanı sıfır

        # 4. Gantt Chart çizimi
        fig, ax = plt.subplots(figsize=(12, 6))
        colors = cm.get_cmap('tab20', len(Job_Number))

        for machine_id, schedule in enumerate(machine_schedules):
            current_time = 0
            for job, start_time, processing_time in schedule:
                ax.barh(machine_id, processing_time, left=start_time, 
                    height=0.3, align='center', 
                    color=colors(job-1), edgecolor='black')
                
                # Job etiketlerini ekle
                ax.text(start_time + processing_time/2, machine_id,
                        f'Job {job}', ha='center', va='center')

        # Cutting point bilgisi ekle
        ax.axvline(x=cutting_point, color='red', linestyle='--', label='Cutting Point')

        # Makespan hesapla
        makespan = cutting_point  # Calculate makespan
        ax.text(makespan, num_machines, f'Makespan: {makespan:.2f}', 
                color='blue', ha='center', va='bottom')

        # Plot'u özelleştir
        ax.set_xlabel('Time')
        ax.set_ylabel('Machines')
        ax.set_title('Parallel Machine Schedule (Preemption Included)')
        ax.set_ylim(-0.5, num_machines-0.5)
        ax.set_yticks(range(num_machines))
        ax.set_yticklabels([f'Machine {i+1}' for i in range(num_machines)])
        ax.grid(True)
        ax.legend()  # Add legend to show cutting point

        plt.tight_layout()
        plt.show()

