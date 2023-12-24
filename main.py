import random
import math

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

def greedy_hill_climbing_with_iterations(initial_state):
    current_state = initial_state
    iterations = 0
    while True:
        iterations += 1
        neighbors = get_neighbors(current_state)
        next_state = min(neighbors, key=conflicts)
        if conflicts(next_state) >= conflicts(current_state):
            return current_state, iterations
        current_state = next_state

def sideways_move_hill_climbing_with_iterations(initial_state, max_sideways_moves=100):
    current_state = initial_state
    iterations = 0
    sideways_moves = 0
    while True:
        iterations += 1
        neighbors = get_neighbors(current_state)
        next_state = min(neighbors, key=conflicts)
        if conflicts(next_state) < conflicts(current_state):
            current_state = next_state
            sideways_moves = 0
        elif conflicts(next_state) == conflicts(current_state) and sideways_moves < max_sideways_moves:
            current_state = next_state
            sideways_moves += 1
        else:
            return current_state, iterations

def random_restart_hill_climbing_with_iterations():
    iterations = 0
    best_conflicts = float('inf')
    while best_conflicts != 0:
        iterations += 1
        initial_state = [random.randint(0, 7) for _ in range(8)]
        state = greedy_hill_climbing_with_iterations(initial_state)[0]
        current_conflicts = conflicts(state)
        if current_conflicts < best_conflicts:
            best_conflicts = current_conflicts
            best_state = state
    return best_state, iterations

def simulated_annealing_with_iterations(initial_state):
    current_state = initial_state
    iterations = 0
    temperature = 1.0
    cooling_rate = 0.99
    min_temperature = 0.01

    while temperature > min_temperature:
        iterations += 1
        neighbor = random.choice(get_neighbors(current_state))
        neighbor_conflicts = conflicts(neighbor)
        if neighbor_conflicts < conflicts(current_state):
            probability = 1.0
        else:
            probability = math.exp(-(neighbor_conflicts - conflicts(current_state)) / temperature)
        if random.random() < probability:
            current_state = neighbor
        temperature *= cooling_rate

    return current_state, iterations

def run_experiment(algorithm, num_runs, is_random_restart=False):
    """ Run the given algorithm multiple times and collect statistics """
    success_count = 0
    total_iterations = 0
    for _ in range(num_runs):
        if is_random_restart:
            result, iterations = algorithm()
        else:
            initial_state = [random.randint(0, 7) for _ in range(8)]
            result, iterations = algorithm(initial_state)
        if conflicts(result) == 0:
            success_count += 1
            total_iterations += iterations
    return success_count, total_iterations / success_count if success_count > 0 else 0

# Run experiments for each algorithm
num_runs = 100
greedy_stats = run_experiment(greedy_hill_climbing_with_iterations, num_runs)
sideways_stats = run_experiment(sideways_move_hill_climbing_with_iterations, num_runs)
random_restart_stats = run_experiment(random_restart_hill_climbing_with_iterations, num_runs, is_random_restart=True)
simulated_annealing_stats = run_experiment(simulated_annealing_with_iterations, num_runs)

# Print the results
print("Greedy Hill Climbing:", greedy_stats)
print("Sideways Move Hill Climbing:", sideways_stats)
print("Random Restart Hill Climbing:", random_restart_stats)
print("Simulated Annealing:", simulated_annealing_stats)
