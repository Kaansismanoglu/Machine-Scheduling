import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def Flow_Shop_Approximation_Algorithms(file_path, num_machines, selected_rule):
    # Read the data file
    data = pd.read_excel(file_path, engine='openpyxl')
    Job_Number = data['Job Number']
    Processing_Times = data[[f'Processing Time for Machine {i}' for i in range(1, num_machines+1)]]
    Weights = data['weight']
    
    if selected_rule == "Decomposition Algorithm (m/2)":
        # Is it possible to implement this algorithm?
        if num_machines % 2 != 0:
            raise ValueError("Decomposition Algorithm (m/2) is only applicable for even number of machines.")
        else:
            Machine_Groups = []
            group_size = 2  # Each group contains pairs of machines

            for i in range(0, num_machines, group_size):
                Machine_Groups.append(tuple(f'Machine {j + 1}' for j in range(i, i + group_size)))

            print(Machine_Groups)
            
        # Gruplara göre sıralama
        group_schedules = {}  # Her grup için iş sıralamaları

        for group in Machine_Groups:
            machine_1 = group[0]
            machine_2 = group[1]

            # İşleri SPT ve LPT'ye göre ayır ve sırala
            jobs_spt = []  # SPT için işler
            jobs_lpt = []  # LPT için işler
            for k in range(len(Job_Number)):
                job = Job_Number[k]
                if Processing_Times[f'Processing Time for {machine_1}'][k] <= Processing_Times[f'Processing Time for {machine_2}'][k]:
                    jobs_spt.append((job, Processing_Times[f'Processing Time for {machine_1}'][k]))
                else:
                    jobs_lpt.append((job, Processing_Times[f'Processing Time for {machine_2}'][k]))

            # SPT ve LPT'ye göre sıralama
            jobs_spt = sorted(jobs_spt, key=lambda x: x[1])  # İşlem süresine göre artan
            jobs_lpt = sorted(jobs_lpt, key=lambda x: x[1], reverse=True)  # İşlem süresine göre azalan

            # Sıralanan işleri birleştir
            group_jobs = [job[0] for job in jobs_spt] + [job[0] for job in jobs_lpt]
            group_schedules[group] = group_jobs

        # Gantt Chart için işlerin işlenme zamanlarını hesaplama (Flow Shop)
        flow_schedule = {f'Machine {i + 1}': [] for i in range(num_machines)}
        current_time = [0] * num_machines  # Her makinenin başlangıç zamanı

        Time_of_Jobs = {}
        
        total_completion_time = 0
        total_weighted_completion_time = 0  # Initialize total weighted completion time
        total_tardiness = 0  # Initialize total tardiness
        total_weighted_tardiness = 0  # Initialize total weighted tardiness
        total_lateness = 0  # Initialize total lateness
        
        for group, jobs in group_schedules.items():
            for job in jobs:
                for machine_name in group:
                    machine_idx = int(machine_name.split()[-1]) - 1
                    job_time = Processing_Times[f'Processing Time for {machine_name}'][job - 1]

                    # Start time depends on the previous job's end time on this machine
                    # and the job's end time on any other machine it's been processed on
                    if job in Time_of_Jobs:
                        # Get the latest end time among all machines this job has been processed on
                        last_machine_end_time = max(Time_of_Jobs[job][m][1] for m in Time_of_Jobs[job])
                        start_time = max(current_time[machine_idx], last_machine_end_time)
                    else:
                        start_time = current_time[machine_idx]  # No prior processing; use current time

                    end_time = start_time + job_time
                    
                    total_completion_time = end_time + total_completion_time

                    # Store the start and end times for the job on the current machine
                    if job not in Time_of_Jobs:
                        Time_of_Jobs[job] = {}
                    Time_of_Jobs[job][machine_name] = (start_time, end_time)

                    # Append the job's timing to the flow schedule for the current machine
                    flow_schedule[machine_name].append((f'Job {job}', start_time, end_time))

                    # Update the current time for the machine
                    current_time[machine_idx] = end_time
                # Update total weighted completion time only with the end time of the last machine in the last group
                if machine_name == group[-1] and group == list(group_schedules.keys())[-1]:  # Check if it's the last machine in the last group
                    # Calculate total weighted completion time
                    print("Job: ", job)
                    print("Weight: ", Weights[job - 1])
                    print("End Time: ", end_time)
                    
                    # Calculate tardiness for the job
                    due_date = data['due date '][job - 1]  # Assuming due date is in the data
                    tardiness = max(0, end_time - due_date)
                    total_tardiness += tardiness  # Accumulate total tardiness
                    
                    total_weighted_completion_time += end_time * Weights[job - 1]  # Add weighted completion time for the job
                    total_weighted_tardiness += tardiness * Weights[job - 1]  # Add weighted tardiness for the job
                    
                    # Calculate lateness for the job
                    lateness = end_time - due_date
                    total_lateness += lateness  # Accumulate total lateness
                    
        print("Flow Schedule: ", flow_schedule)
        print("Current Time: ", current_time)
        print("Total Tardiness: ", total_tardiness)  # Print total tardiness
        print("Total Weighted Tardiness: ", total_weighted_tardiness)  # Print total weighted tardiness
        print("Total Lateness: ", total_lateness)  # Print total lateness

        # Gantt Chart çizimi
        fig, ax = plt.subplots(figsize=(12, 8))
        colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#C2C2C2']
        color_index = 0

        for machine, schedule in flow_schedule.items():
            for job, start, end in schedule:
                ax.barh(machine, end - start, left=start, color=colors[color_index % len(colors)], edgecolor='black')
                ax.text((start + end) / 2, machine, f'{job}', va='center', ha='center', color='black')
            color_index += 1

        makespan = max(current_time)

        print("Total Completion Time: ", total_completion_time)
        print("Total Weighted Completion Time: ", total_weighted_completion_time)  # Print total weighted completion time
        print("Makespan: ", makespan)

        # Adding labels for total completion time, total weighted completion time, makespan, total tardiness, total weighted tardiness, and total lateness on the same ax
        ax.text(0.5, -0.1, f'Total Completion Time: {total_completion_time}', transform=ax.transAxes, ha='center', fontsize=10)
        ax.text(0.5, -0.15, f'Total Weighted Completion Time: {total_weighted_completion_time}', transform=ax.transAxes, ha='center', fontsize=10)  # Add total weighted completion time
        ax.text(0.5, -0.2, f'Makespan: {makespan}', transform=ax.transAxes, ha='center', fontsize=10)
        ax.text(0.5, -0.25, f'Total Tardiness: {total_tardiness}', transform=ax.transAxes, ha='center', fontsize=10)  # Add total tardiness
        ax.text(0.5, -0.3, f'Total Weighted Tardiness: {total_weighted_tardiness}', transform=ax.transAxes, ha='center', fontsize=10)  # Add total weighted tardiness
        ax.text(0.5, -0.35, f'Total Lateness: {total_lateness}', transform=ax.transAxes, ha='center', fontsize=10)  # Add total lateness
        ax.set_xlabel('Time')
        ax.set_ylabel('Machines')
        ax.set_title('Gantt Chart for Flow Shop')
        plt.tight_layout()
        plt.show()
        
        
    elif selected_rule == "Aggregation Algorithm (m/2)":
        # Is it possible to implement this algorithm?
        if num_machines % 2 != 0:
            raise ValueError("Aggregation Algorithm (m/2) is only applicable for even number of machines.")
        else:
            Machine_Groups = []
            group_size = num_machines // 2  # Each group contains half of the machines
            
            for i in range(0, num_machines, group_size):
                Machine_Groups.append(tuple(f'Machine {j + 1}' for j in range(i, i + group_size)))
                                      
            #Summation of processing times for each job for Group 1 and Group 2
            sum_processing_times_group1 = []
            sum_processing_times_group2 = []
            
            for i in range(len(Job_Number)):
                sum_processing_times_group1.append(sum(Processing_Times[f'Processing Time for {machine}'][i] for machine in Machine_Groups[0]))
                sum_processing_times_group2.append(sum(Processing_Times[f'Processing Time for {machine}'][i] for machine in Machine_Groups[1]))
                
            #Choose the group with the minimum processing time
            group_schedules = {}
            spt_schedule = []  # Changed to a list to allow appending
            lpt_schedule = []  # Changed to a list to allow appending
            
            for i in range(len(Job_Number)):
                if sum_processing_times_group1[i] <= sum_processing_times_group2[i]:
                    group_schedules[Job_Number[i]] = Machine_Groups[0]
                    spt_schedule.append((Job_Number[i], sum_processing_times_group1[i]))  # Append as a tuple
                else:
                    group_schedules[Job_Number[i]] = Machine_Groups[1]
                    lpt_schedule.append((Job_Number[i], sum_processing_times_group2[i]))  # Append as a tuple
                    
            # Sorting SPT and LPT schedules
            spt_schedule = sorted(spt_schedule, key=lambda x: x[1])
            lpt_schedule = sorted(lpt_schedule, key=lambda x: x[1], reverse=True)
            
            # Combine the sorted schedules and print jobs with their processing times
            combined_schedules = [spt_schedule[i][0] for i in range(len(spt_schedule))] + \
                                  [lpt_schedule[i][0] for i in range(len(lpt_schedule))]
            
            # Gantt Chart için işlerin işlenme zamanlarını hesaplama (Flow Shop)
            # Now, we will process all jobs based on the combined schedule
            flow_schedule = {f'Machine {i + 1}': [] for i in range(num_machines)}
            current_time = [0] * num_machines  # Initialize start time for each machine
            Time_of_Jobs = {}  # Dictionary to store the times of jobs

            # Process each job in the combined schedule (for all machines)
            total_completion_time = 0
            total_weighted_completion_time = 0  # Initialize total weighted completion time
            total_tardiness = 0  # Initialize total tardiness
            total_weighted_tardiness = 0  # Initialize total weighted tardiness
            total_lateness = 0  # Initialize total lateness
            
            for job in combined_schedules:
                # Process each job for all machines
                for machine_idx in range(num_machines):
                    machine_name = f'Machine {machine_idx + 1}'
                    job_time = Processing_Times[f'Processing Time for {machine_name}'][job - 1]  # Assuming `job` is 1-indexed
                    
                    if job in Time_of_Jobs:
                        last_machine_end_time = max(Time_of_Jobs[job][m][1] for m in Time_of_Jobs[job])
                        start_time = max(current_time[machine_idx], last_machine_end_time)
                    else:
                        start_time = current_time[machine_idx]

                    end_time = start_time + job_time

                    if job not in Time_of_Jobs:
                        Time_of_Jobs[job] = {}
                    Time_of_Jobs[job][machine_name] = (start_time, end_time)

                    flow_schedule[machine_name].append((f'Job {job}', start_time, end_time))
                    current_time[machine_idx] = end_time

                    # Calculate total weighted completion time based on the last machine's end time
                    if machine_idx == num_machines - 1:  # Only for the last machine
                        total_completion_time += end_time  # Corrected accumulation of total completion time
                        total_weighted_completion_time += end_time * Weights[job - 1]  # Add weighted completion time for the job
                        
                        # Calculate tardiness for the job
                        due_date = data['due date '][job - 1]  # Assuming due date is in the data
                        tardiness = max(0, end_time - due_date)
                        total_tardiness += tardiness  # Accumulate total tardiness
                        total_weighted_tardiness += tardiness * Weights[job - 1]  # Add weighted tardiness for the job
                        
                        # Calculate lateness for the job
                        lateness = end_time - due_date
                        total_lateness += lateness  # Accumulate total lateness

            # Final Outputs
            print("Flow Schedule:", flow_schedule)
            print("Current Time:", current_time)

            # Calculate Makespan
            makespan = max(current_time)

            print("Total Completion Time:", total_completion_time)
            print("Total Weighted Completion Time:", total_weighted_completion_time)  # Print total weighted completion time
            print("Total Tardiness:", total_tardiness)  # Print total tardiness
            print("Total Weighted Tardiness:", total_weighted_tardiness)  # Print total weighted tardiness
            print("Total Lateness:", total_lateness)  # Print total lateness
            print("Makespan:", makespan)

            fig, ax = plt.subplots(figsize=(12, 8))
            colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#C2C2C2']
            color_index = 0

            for machine, schedule in flow_schedule.items():
                for job, start, end in schedule:
                    ax.barh(machine, end - start, left=start, color=colors[color_index % len(colors)], edgecolor='black')
                    ax.text((start + end) / 2, machine, f'{job}', va='center', ha='center', color='black')
                color_index += 1

            ax.text(0.5, -0.1, f'Total Completion Time: {total_completion_time}', transform=ax.transAxes, ha='center', fontsize=10)
            ax.text(0.5, -0.15, f'Total Weighted Completion Time: {total_weighted_completion_time}', transform=ax.transAxes, ha='center', fontsize=10)  # Add total weighted completion time
            ax.text(0.5, -0.2, f'Makespan: {makespan}', transform=ax.transAxes, ha='center', fontsize=10)
            ax.text(0.5, -0.25, f'Total Tardiness: {total_tardiness}', transform=ax.transAxes, ha='center', fontsize=10)  # Add total tardiness
            ax.text(0.5, -0.3, f'Total Weighted Tardiness: {total_weighted_tardiness}', transform=ax.transAxes, ha='center', fontsize=10)  # Add total weighted tardiness
            ax.text(0.5, -0.35, f'Total Lateness: {total_lateness}', transform=ax.transAxes, ha='center', fontsize=10)  # Add total lateness
            ax.set_xlabel('Time')
            ax.set_ylabel('Machines')
            ax.set_title('Gantt Chart for Flow Shop')
            plt.tight_layout()
            plt.show()
    else:
        raise ValueError("Invalid dispatching rule selected.")
