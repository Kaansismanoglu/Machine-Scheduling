# Machine Scheduling Application

## Introduction

This project focuses on solving machine scheduling problems, leveraging a combination of dispatching rules, approximate algorithms, and local search techniques to optimize resource usage in production systems. The primary goal is to enhance efficiency, reduce costs, and streamline scheduling processes by distributing resources effectively.

The application developed provides:
- Real-time decision-making capabilities through dispatching rules.
- Heuristic-based and approximation methods for near-optimal solutions.
- An intuitive interface for user-friendly operations.

## Features

### 1. User-Friendly Interface
- Clean coding principles for maintainability.
- Sidebar navigation for easy access to functionalities.
- Appearance Mode and UI Scaling for an enhanced user experience.

### 2. Scheduling Environments
- **Single Machine**: Optimize scheduling for a single machine setup.
- **Parallel Machine**: Manage tasks across multiple machines.
- **Flow Shop**: Sequence jobs across multiple machines in a specific order.

### 3. Objectives
The application supports the following scheduling objectives:
- Makespan (Maximum Completion Time)
- Total Completion Time
- Total Weighted Completion Time
- Total Tardiness
- Total Weighted Tardiness
- Total Lateness
- Number of Tardy Jobs

### 4. Algorithms and Techniques
- **Dispatching Rules**: SPT, LPT, EDD, WSPT, SRPT, and more.
- **Approximation Algorithms**: Johnson’s Algorithm, Decomposition Algorithm, Aggregation Algorithm.
- **Local Search**: Iterative improvement for better solutions, with constraints like iteration limits or running time.

## Input

The application accepts data in two Excel formats:

1. **Single and Parallel Machine**: `input_format_for_project.xlsx`
   - Fields: Job Number, Process Time, Due Date, Weight, Release Date.

2. **Flow Shop**: `FlowShopData.xlsx`
   - Fields: Job Number, Processing Time for each Machine, Due Date, Weight, Release Date.

Users can customize these files and upload them through the application. For Flow Shop, additional columns can be added for more machines.

## Output

The application automatically calculates and visualizes results based on the selected inputs and objectives:
- Gantt charts to represent scheduling results.
- Transparent and traceable iteration results for local search algorithms.
- Detailed calculations displayed in real-time.

### Example Outputs
- **Parallel Machine**: Wrap-Around technique minimizes makespan.
- **Flow Shop**: Decomposition Algorithm provides near-optimal solutions.

## How to Use

1. Upload the appropriate Excel file.
2. Select the desired scheduling environment (Single, Parallel, or Flow Shop).
3. Choose the objective to optimize and input relevant parameters.
4. View results in graphs and Gantt charts.

## Conclusion

This application is a powerful tool for addressing diverse machine scheduling challenges. It balances precision and efficiency, making it suitable for both academic research and industrial applications. With its robust algorithms and user-centric design, the tool simplifies complex scheduling processes and offers actionable insights for optimization.

## Team Members
- **İlkem Nur Akmeriç**
- **Kaan Şişmanoğlu**
- **Efe Toprak Temeroğlu**
