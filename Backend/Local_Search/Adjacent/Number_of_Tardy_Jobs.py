import random
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import time  # Import time module to track runtime

random.seed(42)  # Set a random seed for reproducibility

def calculate_number_of_tardy_jobs(job_sequence, Processing_Times, Due_Date, num_machines):
    # Initialize completion times matrix
    num_jobs = len(job_sequence)
    
    # Initialize machine completion times for each job
    completion_times = [[0] * num_machines for _ in range(num_jobs)]
    
    tardy_jobs_count = 0  # Initialize count of tardy jobs
    
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

    # Calculate number of tardy jobs
    for job_index in range(num_jobs):
        completion_time = completion_times[job_index][-1]  # Completion time on the last machine
        due_date = Due_Date.iloc[job_sequence[job_index] - 1]  # Get due date for the job using the job_sequence
        
        if completion_time > due_date:  # Check if the job is tardy
            tardy_jobs_count += 1  # Increment the count of tardy jobs
    
    return tardy_jobs_count

# Swap a job with a randomly selected adjacent job in the job sequence
def swap_with_random_adjacent(job_sequence):
    i = random.randint(0, len(job_sequence) - 2)  # Select a random index for the job to swap
    job_sequence[i], job_sequence[i + 1] = job_sequence[i + 1], job_sequence[i]
    return job_sequence

def Number_of_Tardy_Jobs_Adjacent(Processing_Times, job_sequence, Due_Date, num_machines, iterations=None, runtime=None):
    start_iteration_time = time.time()  # Start time tracking
    current_tardy_jobs_count = calculate_number_of_tardy_jobs(job_sequence, Processing_Times, Due_Date, num_machines)  # Calculate initial number of tardy jobs
    
    output_lines = []  # List to store output lines for the text file
    output_lines.append(f"Initial Solution: {job_sequence}, Number of Tardy Jobs: {current_tardy_jobs_count}\n")
    output_lines.append("-----------------------------\n")
    
    best_solution = job_sequence.copy()  # Initialize best solution with the initial job sequence

    iteration_count = 0
    
    while True:  # Continue indefinitely
        output_lines.append("Swapping with a random adjacent job\n")
        
        # Create a new sequence by swapping randomly
        new_sequence = swap_with_random_adjacent(job_sequence.copy())
        
        new_tardy_jobs_count = calculate_number_of_tardy_jobs(new_sequence, Processing_Times, Due_Date, num_machines)  # Calculate number of tardy jobs after swap
        
        if new_tardy_jobs_count <= current_tardy_jobs_count:  # Check if the new count of tardy jobs is better
            current_tardy_jobs_count = new_tardy_jobs_count  # Update current count of tardy jobs
            job_sequence = new_sequence.copy()  # Update current sequence
            best_solution = new_sequence.copy()  # Update best solution
            output_lines.append(f"Iteration: {iteration_count}, New Best Solution: {new_sequence}, Number of Tardy Jobs: {new_tardy_jobs_count}\n")
            output_lines.append("------------Updated-------------\n")
            
            iteration_count += 1
        else:
            output_lines.append(f"Iteration: {iteration_count}, Worse Solution: {new_sequence}, Number of Tardy Jobs: {new_tardy_jobs_count}\n")
            output_lines.append("VS.\n")
            output_lines.append(f"Current Best Solution: {best_solution}, Number of Tardy Jobs: {current_tardy_jobs_count}\n")
            output_lines.append("-----------Not Updated-------------\n")
            
            iteration_count += 1
        
        # Apply iteration limit or runtime limit
        if (iterations is not None and iteration_count >= iterations) or (runtime is not None and (time.time() - start_iteration_time) >= runtime):
            break
    
    end_time = time.time()  # End time tracking
    runtime = end_time - start_iteration_time

    # Convert runtime to hours, minutes, and seconds
    hours, remainder = divmod(runtime, 3600)
    minutes, seconds = divmod(remainder, 60)

    # Update output
    output_lines.append(f"Runtime: {int(hours)}h {int(minutes)}m {seconds:.2f}s\n")  # More readable format
    

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
    
    # Adding due dates to the Gantt chart
    num_jobs = len(job_sequence)  # Define num_jobs here
    due_colors = cm.get_cmap('tab20', num_jobs)  # Use a different colormap for due dates with more distinct colors
    for job_index in range(num_jobs):
        due_date = Due_Date.iloc[job_index]
        gnt.axvline(x=due_date, color=due_colors(job_index), linestyle='--', label=f'Due Date Job {job_index + 1}')
    
    # Adding machine labels without y-axis values
    for machine in range(num_machines):
        gnt.text(-1, machine + 0.5, f'Machine {machine + 1}', ha='right', va='center', color='black')

    gnt.yaxis.set_visible(False)  # Hide y-axis values

    plt.title('Gantt Chart for Job Scheduling')
    plt.text(completion_times[-1][-1] / 2, num_machines + 0.5, f'Number of Tardy Jobs: {current_tardy_jobs_count}', 
             ha='center', va='center', fontsize=12, color='red')  # Add number of tardy jobs value to the chart
    plt.text(completion_times[-1][-1] / 2, num_machines + 1.5, f'Runtime: {runtime:.2f} seconds', 
             ha='center', va='center', fontsize=12, color='blue')  # Add runtime value to the chart
    plt.legend(loc='upper left')  # Show legend for due dates and position it to the upper left
    plt.show()

    # Write output to a text file
    with open("number_of_tardy_jobs_output.txt", "w") as f:
        f.writelines(output_lines)
    
    return best_solution  # Return the best solution found
