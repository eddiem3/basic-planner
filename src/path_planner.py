import ompl.base as ob
import ompl.geometric as og
import matplotlib.pyplot as plt
import csv
import datetime

# Load obstacles from "obstacles.csv" file
obstacles = []
with open('obstacles.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        x, y = map(float, row)
        obstacles.append((x, y))

# Create an OMPL state space for 2D planning
space = ob.RealVectorStateSpace(2)
bounds = ob.RealVectorBounds(2)
bounds.setLow(0)
bounds.setHigh(100)
space.setBounds(bounds)

# Create a space information structure
si = ob.SpaceInformation(space)

# Create a state validity checker that accounts for obstacles
class StateValidityChecker(ob.StateValidityChecker):
    def isValid(self, state):
        for obstacle in obstacles:
            x, y = obstacle
            dx = state[0] - x
            dy = state[1] - y
            if dx**2 + dy**2 <= 5**2:  # Obstacle is a circle with radius 5
                return False
        return True

si.setStateValidityChecker(StateValidityChecker(si))

# Create a start and goal state
start = ob.State(space)
start[0] = 0
start[1] = 0

goal = ob.State(space)
goal[0] = 100
goal[1] = 100

# Create a simple setup and set the start and goal states
ss = og.SimpleSetup(si)
ss.setStartState(start)
ss.setGoalState(goal)

# Set the planner
planner = og.RRT(si)
ss.setPlanner(planner)

# Perform motion planning
ss.solve(10.0)

# Display the path
path = ss.getSolutionPath()
path.interpolate()
path_states = path.getStates()
path_x = [state[0] for state in path_states]
path_y = [state[1] for state in path_states]

# Create a scatter plot with circles for obstacles and a plot for the path
fig, ax = plt.subplots()
for obstacle in obstacles:
    x, y = obstacle
    circle = plt.Circle((x, y), 5, fill=False, color='red')
    ax.add_artist(circle)

plt.plot(path_x, path_y, marker='o', linestyle='-', color='blue', markersize=5)
plt.xlim(0, 100)
plt.ylim(0, 100)
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Path Planning with Obstacles')
plt.grid(True)

# Set the major gridlines to be at intervals of 1 unit
plt.xticks(range(0, 101, 1))
plt.yticks(range(0, 101, 1))

# Append the current date and time to the file name
current_datetime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
file_name = f'path_plot_{current_datetime}.png'

# Save the plot to the file with the appended date and time
plt.savefig(file_name, dpi=300)  # Save as a high-resolution PNG file

plt.show()

