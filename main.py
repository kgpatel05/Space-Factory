from collections import deque

class Graph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, u: str, v: tuple):
        """
        Add an edge to the graph.
        :param u: The transition identifier (e.g., 'trans_0').
        :param v: A tuple containing (inputs, outputs).
        """
        self.graph[u] = v  # Store only (inputs, outputs) without weights

    def print_graph(self):
        for u, (inputs, outputs) in self.graph.items():
            print(f"Node: {u}, Transformation: ({inputs}, {outputs})")


def read_input() -> tuple:  
    try:
        numtransitions = int(input("Enter the number of transitions: "))
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return None, None, None

    transitions = []
    
    for i in range(1, numtransitions + 1):
        while True:  # Keep asking until a valid transition is entered
            transition = input(f"Enter transition {i}: ").strip()
            if "->" in transition:
                transitions.append(transition)
                break
            else:
                print("Invalid format. Please include '->' in the transition.")

    try:
        supplies = input("Enter the supplies: ").strip()
        demand = input("Enter the demand: ").strip()
    except ValueError:
        print("Invalid input. Please enter valid supplies and demand.")
        return None, None, None
    
    return transitions, supplies, demand


def process_transitions(transitions: list) -> Graph:
    # Returns a structured graph of all transitions
    transition_table = Graph()

    for index, transition in enumerate(transitions):
        # Split the transition into inputs and outputs
        try:
            inputs, outputs = transition.split("->")
        except ValueError:
            print(f"Invalid transition format: {transition}")
            continue

        inputs = inputs.strip().split()
        outputs = outputs.strip().split()

        # Parse input quantities and items
        input_items = {}
        for i in range(0, len(inputs), 2):  # Step by 2 (quantity, item)
            quantity, item = int(inputs[i]), inputs[i + 1]
            input_items[item] = quantity

        # Parse output quantities and items
        output_items = {}
        for i in range(0, len(outputs), 2):  # Step by 2 (quantity, item)
            quantity, item = int(outputs[i]), outputs[i + 1]
            output_items[item] = quantity

        # Add this transformation as a node in the graph
        transition_table.add_edge(f"trans_{index}", (input_items, output_items))

    return transition_table


def process_supplies(supplies:str) -> dict:
    supply_dict = {}
    supplies = supplies.strip().split()
    for i in range(0, len(supplies), 2):  # Step by 2 (quantity, item)
        quantity, item = int(supplies[i]), supplies[i + 1]
        supply_dict[item] = quantity
    return supply_dict


def process_demand(demand:str) -> dict:
    demand_dict = {}
    demand = demand.strip().split()
    for i in range(0, len(demand), 2):  # Step by 2 (quantity, item)
        quantity, item = int(demand[i]), demand[i + 1]
        demand_dict[item] = quantity
    return demand_dict


def is_demand_met(current_inventory:dict, demand:dict) -> bool:
    for item, quantity in demand.items():
        if current_inventory.get(item, 0) < quantity:
            return False
    return True


def can_apply_transformation(current_inventory:dict, inputs:dict) -> bool:
    for item, quantity in inputs.items():
        if current_inventory.get(item, 0) < quantity:
            return False
    return True


def apply_transformation(current_inventory:dict, inputs:dict, outputs:dict) -> dict:
    new_inventory = current_inventory.copy()
    for item, quantity in inputs.items():
        new_inventory[item] -= quantity
    for item, quantity in outputs.items():
        new_inventory[item] = new_inventory.get(item, 0) + quantity
    return new_inventory


def find_shortest_transformation_sequence(graph:Graph, supplies:dict, demand:dict):
    queue = deque([(supplies, [])])
    visited = set()
    visited.add(tuple(sorted(supplies.items())))

    while queue:
        current_inventory, sequence = queue.popleft()

        if is_demand_met(current_inventory, demand):
            return sequence

        for idx, (inputs, outputs) in enumerate(graph.graph.values()):
            if can_apply_transformation(current_inventory, inputs):
                new_inventory = apply_transformation(current_inventory, inputs, outputs)
                serialized_inventory = tuple(sorted(new_inventory.items()))
                if serialized_inventory not in visited:
                    visited.add(serialized_inventory)
                    queue.append((new_inventory, sequence + [idx + 1]))

    return "No solution"

def driver():
    transitions, supplies, demand = read_input()
    if transitions is not None:
        transition_graph = process_transitions(transitions)
        supply_dict = process_supplies(supplies)
        demand_dict = process_demand(demand)
        result = find_shortest_transformation_sequence(transition_graph, supply_dict, demand_dict)
        print(result)
        return result

if __name__ == "__main__":
    driver()
