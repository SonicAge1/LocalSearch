import random
import math
import matplotlib.pyplot as plt

def conflicts(state):
    """ Count the number of conflicts in the state """
    num_conflicts = 0
    for i in range(len(state)):
        for j in range(i + 1, len(state)):
            if state[i] == state[j] or abs(state[i] - state[j]) == j - i:
                num_conflicts += 1
    return num_conflicts

def get_neighbors(state):
    """ Generate neighbors by moving each queen to another row in the same column """
    neighbors = []
    for i in range(len(state)):
        for j in range(len(state)):
            if state[i] != j:
                neighbor = list(state)
                neighbor[i] = j
                neighbors.append(neighbor)
    return neighbors

def greedy_hill_climbing_with_trace(initial_state):
    current_state = initial_state
    trace = [conflicts(current_state)]
    while True:
        neighbors = get_neighbors(current_state)
        next_state = min(neighbors, key=conflicts)
        if conflicts(next_state) >= conflicts(current_state):
            return trace
        current_state = next_state
        trace.append(conflicts(current_state))

def sideways_move_hill_climbing_with_trace(initial_state, max_sideways_moves=100):
    current_state = initial_state
    sideways_moves = 0
    trace = [conflicts(current_state)]
    while True:
        neighbors = get_neighbors(current_state)
        next_state = min(neighbors, key=conflicts)
        if conflicts(next_state) < conflicts(current_state):
            current_state = next_state
            sideways_moves = 0
        elif conflicts(next_state) == conflicts(current_state) and sideways_moves < max_sideways_moves:
            current_state = next_state
            sideways_moves += 1
        else:
            return trace
        trace.append(conflicts(current_state))

def random_restart_hill_climbing_with_trace():
    best_state = None
    best_conflicts = float('inf')
    trace = []
    while best_conflicts != 0:
        initial_state = [random.randint(0, 7) for _ in range(8)]
        state_trace = greedy_hill_climbing_with_trace(initial_state)  # 只接收一个值
        current_conflicts = state_trace[-1]  # 获取最后一个状态的冲突数
        trace.extend(state_trace)
        if current_conflicts < best_conflicts:
            best_conflicts = current_conflicts
            best_state = initial_state  # 或者调整为记录当前最优状态
    return trace


def simulated_annealing_with_trace(initial_state):
    current_state = initial_state
    temperature = 1.0
    cooling_rate = 0.99
    min_temperature = 0.01
    trace = [conflicts(current_state)]
    while temperature > min_temperature:
        neighbor = random.choice(get_neighbors(current_state))
        neighbor_conflicts = conflicts(neighbor)
        if neighbor_conflicts < conflicts(current_state):
            probability = 1.0
        else:
            probability = math.exp(-(neighbor_conflicts - conflicts(current_state)) / temperature)
        if random.random() < probability:
            current_state = neighbor
        temperature *= cooling_rate
        trace.append(conflicts(current_state))
    return trace

# We will run each algorithm 100 times and average their traces to obtain a smoother convergence curve.

def average_traces(traces):
    """ Average the collected traces over multiple runs. """
    max_length = max(map(len, traces))
    # Extend all traces to the maximum length to allow averaging
    extended_traces = [trace + [trace[-1]] * (max_length - len(trace)) for trace in traces]
    # Calculate the average at each step
    average_trace = [sum(steps) / len(steps) for steps in zip(*extended_traces)]
    return average_trace

# Run each algorithm 100 times
num_runs = 1000
all_greedy_traces = [greedy_hill_climbing_with_trace([random.randint(0, 7) for _ in range(8)]) for _ in range(num_runs)]
all_sideways_traces = [sideways_move_hill_climbing_with_trace([random.randint(0, 7) for _ in range(8)]) for _ in range(num_runs)]
all_random_restart_traces = [random_restart_hill_climbing_with_trace() for _ in range(num_runs)]
all_simulated_annealing_traces = [simulated_annealing_with_trace([random.randint(0, 7) for _ in range(8)]) for _ in range(num_runs)]

# Average the traces
average_greedy_trace = average_traces(all_greedy_traces)
average_sideways_trace = average_traces(all_sideways_traces)
average_random_restart_trace = average_traces(all_random_restart_traces)
average_simulated_annealing_trace = average_traces(all_simulated_annealing_traces)

# Plotting the average convergence curves
plt.figure(figsize=(14, 7))

# Plot the average convergence for each algorithm
plt.plot(average_sideways_trace, label='Average Sideways Move Hill Climbing', color='green')
plt.plot(average_random_restart_trace, label='Average Random Restart Hill Climbing', color='red')
plt.plot(average_greedy_trace, label='Average Greedy Hill Climbing', color='blue')
plt.plot(average_simulated_annealing_trace, label='Average Simulated Annealing', color='purple')

plt.xlabel("Iterations")
plt.ylabel("Average Number of Conflicts")
plt.title("Average Convergence Curves of Different Algorithms")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
