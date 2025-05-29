# User Manual – Job Shop Scheduling with Ant Colony Optimization

## 1. Introduction
This application solves the Job-Shop Scheduling Problem (JSSP) using the Ant Colony Optimization (ACO) algorithm. It provides a graphical user interface (GUI) where users can define jobs, machines, and operations, and visualize the optimized schedule.

## 2. Application Launch
To start the application, run the following command in the terminal:

![image](https://github.com/user-attachments/assets/dcefb6ba-d411-4075-b593-d5b814ee909f)

## 3. Main Window Overview
Once the application opens, you will see the following sections:
Job/Operation/Machine input area (top-left)
ACO parameter input area (top-center)
Control buttons: "Random Fill", "Create Problem", "Start Scheduler", "Stop Scheduler"
Editable job table
Schedule visualization area (bottom)

## 4. Step-by-Step Usage
### Step 1 – Define Problem Size
Enter the number of:

Jobs

Operations per job

Machines

Then click "Create Problem".

### Step 2 – Fill Operation Times
You can either manually enter processing times for each operation-machine combination in the table,

Or click "Random Fill" to populate the table with random processing times.

Each cell represents the time required to process a specific operation of a job on a machine.

### Step 3 – Set ACO Parameters
Adjust the following parameters:

Ants: Number of ants used per iteration

Iterations: Total number of optimization cycles

Evaporation %: Rate of pheromone decay

Alpha: Influence of pheromone trail

Beta: Influence of heuristic (processing time)

### Step 4 – Run the Optimizer
Click the "Start Scheduler" button.

The program will:

Construct multiple solutions using ants,

Update pheromones iteratively,

Display the best-found schedule.

![image](https://github.com/user-attachments/assets/310e08f0-d683-4ec0-ad32-71444af8fb27)

## 5. Output: Schedule Visualization
At the bottom of the window, a Gantt-style chart will appear:

X-axis: Time

Y-axis: Machines

Each bar: A scheduled operation (with job ID and operation index)

Colors represent different jobs. This helps quickly identify overlaps and idle times.

![image](https://github.com/user-attachments/assets/01b98c34-983d-4da7-8d2d-6415afa884a8)

