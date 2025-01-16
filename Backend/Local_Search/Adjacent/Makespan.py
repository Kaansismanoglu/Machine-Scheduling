import random
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import time  # Import time module to track runtime

random.seed(42)  # Set a random seed for reproducibility

def calculate_makespan(job_sequence, Processing_Times, num_machines):
    # Initialize completion times matrix
    num_jobs = len(job_sequence)
    
    # Initialize machine completion times for each job
    completion_times = [[0] * num_machines for _ in range(num_jobs)]
    
    for job_index, job in enumerate(job_sequence):
        for machine in range(num_machines):
            processing_time = Processing_Times.iloc[job - 1, machine]  # Get processing time for the job and machine
            
            if machine == 0:
                # First machine: completion time is cumulative of previous jobs
                completion_times[job_index][machine] = (
                    completion_times[job_index - 1][machine] + processing_time if job_index > 0 else processing_time
                )
            else:
                # General case: max(previous job on this machine, this job on previous machine) + processing time
                completion_times[job_index][machine] = max(
                    completion_times[job_index][machine - 1],  # Job i, Machine j-1
                    completion_times[job_index - 1][machine]   # Job i-1, Machine j
                ) + processing_time
    
    # Makespan is the completion time of the last job on the last machine
    makespan = completion_times[-1][-1]
    return makespan

# Swap a job with a randomly selected adjacent job in the job sequence
def swap_with_random_adjacent(job_sequence):
    i = random.randint(0, len(job_sequence) - 2)  # Select a random index for the job to swap
    job_sequence[i], job_sequence[i + 1] = job_sequence[i + 1], job_sequence[i]
    return job_sequence

def Makespan_Adjacent(Processing_Times, job_sequence, num_machines, iterations=None, runtime=None):
    start_iteration_time = time.time()  # Start time tracking
    
    
    current_makespan = calculate_makespan(job_sequence, Processing_Times, num_machines)  # Calculate initial makespan
    
    output_lines = []  # List to store output lines for the text file
    output_lines.append(f"Initial Solution: {job_sequence}, Makespan: {current_makespan}\n")
    output_lines.append("-----------------------------\n")
    
    best_solution = job_sequence.copy()  # Initialize best solution with the initial job sequence

    iteration_count = 0
    
    while True:  # Continue indefinitely
        output_lines.append("Swapping with a random adjacent job\n")
        
        # Create a new sequence by swapping randomly
        new_sequence = swap_with_random_adjacent(job_sequence.copy())
        
        new_makespan = calculate_makespan(new_sequence, Processing_Times, num_machines)  # Calculate makespan after swap
        
        if new_makespan <= current_makespan:  # Check if the new makespan is better
            current_makespan = new_makespan  # Update current makespan
            job_sequence = new_sequence.copy()  # Update current sequence
            best_solution = new_sequence.copy()  # Update best solution
            output_lines.append(f"Iteration: {iteration_count}, New Best Solution: {new_sequence}, Makespan: {new_makespan}\n")
            output_lines.append("------------Updated-------------\n")
            
            iteration_count += 1
        else:
            output_lines.append(f"Iteration: {iteration_count}, Worse Solution: {new_sequence}, Makespan: {new_makespan}\n")
            output_lines.append("VS.\n")
            output_lines.append(f"Current Best Solution: {best_solution}, Total Completion Time: {current_makespan}\n")
            output_lines.append("-----------Not Updated-------------\n")
            
            iteration_count += 1
        
        if (iterations is not None and iteration_count >= iterations) or (runtime is not None and (time.time() - start_iteration_time) >= runtime):
            break
        
    
    # Gantt chart visualization
    completion_times = [[0] * num_machines for _ in range(len(best_solution))]
    colors = cm.get_cmap('Set2', len(best_solution))  # Use a more harmonious colormap
    for job_index, job in enumerate(best_solution):
        for machine in range(num_machines):
            processing_time = Processing_Times.iloc[job - 1, machine]
            if machine == 0:
                completion_times[job_index][machine] = (
                    completion_times[job_index - 1][machine] + processing_time if job_index > 0 else processing_time
                )
            else:
                completion_times[job_index][machine] = max(
                    completion_times[job_index][machine - 1],
                    completion_times[job_index - 1][machine]
                ) + processing_time


    end_time = time.time()  # End time tracking
    
    
    # Plotting Gantt chart
    fig, gnt = plt.subplots()
    gnt.set_ylim(0, num_machines)
    gnt.set_xlim(0, completion_times[-1][-1])
    gnt.set_xlabel('Time')
    gnt.set_ylabel('Machines')
    
    for job_index, job in enumerate(best_solution):
        for machine in range(num_machines):
            start_time = completion_times[job_index][machine] - Processing_Times.iloc[job - 1, machine]
            gnt.broken_barh([(start_time, Processing_Times.iloc[job - 1, machine])], (machine, 1), facecolors=(colors(job_index)))
            gnt.text(start_time + Processing_Times.iloc[job - 1, machine] / 2, machine + 0.5, f'Job {job}', 
                      ha='center', va='center', color='black')
    
    # Adding machine labels without y-axis values
    for machine in range(num_machines):
        gnt.text(-1, machine + 0.5, f'Machine {machine + 1}', ha='right', va='center', color='black')

    gnt.yaxis.set_visible(False)  # Hide y-axis values

    plt.title('Gantt Chart for Job Scheduling')
    plt.text(completion_times[-1][-1] / 2, num_machines + 0.5, f'Makespan: {current_makespan}', 
             ha='center', va='center', fontsize=12, color='red')  # Add makespan value to the chart
    plt.show()
    
    
    runtime = end_time - start_iteration_time

    # Zamanı saat, dakika ve saniye cinsine dönüştür
    hours, remainder = divmod(runtime, 3600)
    minutes, seconds = divmod(remainder, 60)

    # Çıktıyı güncelle
    output_lines.append(f"Runtime: {int(hours)}h {int(minutes)}m {seconds:.2f}s\n")  # Daha okunabilir format
    
    # Write output to a text file
    with open("makespan_output.txt", "w") as f:
        f.writelines(output_lines)
    
    return best_solution  # Return the best solution found