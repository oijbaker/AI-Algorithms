from math import inf, sqrt
from time import time

# set to 'manhattan' or 'euclidean'
HEURISTIC_TYPE = "manhattan"
open_list = []
closed_list = []
solution = []

START = (7, 2, 4, 5, 0, 6, 8, 3, 1)
GOAL = (0, 1, 2, 3, 4, 5, 6, 7, 8)


def distance_heuristic(node):
    """ 
    calculates the distance heuristic (h-value) for a given node
    
    parameters:
    - node: a 9-tuple containing the board information for a configuration
    """
    
    # the position in which each tile should end up
    position = {
        GOAL[0]: (0, 0),
        GOAL[1]: (0, 1),
        GOAL[2]: (0, 2),
        GOAL[3]: (1, 0),
        GOAL[4]: (1, 1),
        GOAL[5]: (1, 2),
        GOAL[6]: (2, 0),
        GOAL[7]: (2, 1),
        GOAL[8]: (2, 2)
    }
    if HEURISTIC_TYPE == "euclidean":
        # calculate the straight line distance that a tile needs
        # to travel to be in the correct place

        # find the distance between each node and its intended position
        # and add it to the total
        total = 0
        for i in range(9):
            goal_position = position[node[i]]
            actual_position = position[i]
            total += sqrt((goal_position[0]-actual_position[0])**2+
                          (goal_position[1]-actual_position[1])**2)

        return total

    elif HEURISTIC_TYPE == "manhattan":
        """
        find the manhattan distance between the nodes, that is, the straight line
        distance without diagonals
        """

        # find the manhattan distance between each node and its intended position
        # then add it to the total
        total = 0
        for i in range(9):
            goal_position = position[node[i]]
            actual_position = position[i]
            total += (abs(goal_position[0]-actual_position[0])
                     +abs(goal_position[1]-actual_position[1]))

        return total
    else:
        return 0

def find_min():
    """
    find the node with the minimum f value in the open list
    """
    minimum = inf
    min_node = None
    for node in open_list:
        if configurations[node][0] < minimum:
            minimum = configurations[node][0]
            min_node = node
    return min_node

def child(swap, node, blank_index):
    """
    swap two positions in a configuration, and update their values in the configurations
    dictionary, or add the new configuration to the dictionary
    parameters:
    - swap: the new position for the blank tile
    - node: the configuration to work on
    - blank_index: the position of the blank tile
    """
    
    # swap the two positions
    new_config = list(node)
    temp = new_config[blank_index]
    new_config[blank_index] = new_config[swap]
    new_config[swap] = temp
    new_config = tuple(new_config)
    
    # find the distance heuristic
    h = distance_heuristic(new_config)
    
    # if the new configuration (after the swap) is already exisiting,
    # update it's h value, otherwise create a new entry.
    if new_config in configurations.keys():
        configurations[new_config] = [configurations[new_config][0]+h, 0, h, configurations[new_config][3]]
    else:
        configurations[new_config] = [h, 0, h, None]

    return new_config

def expand(node):
    """
    expand a node, and return its children
    
    parameters:
    - node: the configuration to expand
    """
    
    # a dictionary of the possible moves that can be made depending on where the blank space is
    swaps = {
        0: [1, 3],
        1: [0, 2, 4],
        2: [1, 5],
        3: [0, 4, 6],
        4: [1, 3, 5, 7],
        5: [2, 4, 8],
        6: [3, 7],
        7: [4, 6, 8],
        8: [5, 7]
    }

    # for each possible move, make the move and add the result to the list
    children = []

    blank_index = node.index(0)
    for swap in swaps[blank_index]:
        new_child = child(swap, node, blank_index)
        if new_child in configurations.keys():
            children.append(new_child)

    return children

def backtrack(current):
    """ 
    recursively find the solution path by looking through the parents of each child
    """
    if current == None:
        return
    solution.append(current)
    backtrack(configurations[current][3])
    
def next_stage(labels):
    """
    display the next configuration in the solution path
    
    parameters:
    - labels: the labels to display the numbers on
    - sol: the solution path
    """
    
    sol = solution
    config = tuple([int(label["text"]) for label in labels[:9]])
    pos = sol.index(config)

    if config == GOAL:
        labels[9].config(text="Finish")
        return
    elif sol[pos+1] == GOAL:
        labels[9].config(text="Finish")
    else:
        labels[9].config(text="")
        
    for i in range(9):
        if sol[pos+1][i] == 0:
            labels[i].config(text=" ")
        labels[i].config(text=sol[pos+1][i])
        
def prev_stage(labels):
    """
    display the previous configuration in the solution path
    
    parameters:
    - labels: the labels to display the numbers on
    - sol: the solution path
    """
    
    sol = solution
    config = tuple([int(label["text"]) for label in labels[:9]])
    pos = sol.index(config)
    
    if config == START or sol[pos-1] == START:
        labels[9].config(text="Start")
        return
    else:
        labels[9].config(text="")
        
    for i in range(9):
        if sol[pos-1][i] == 0:
            labels[i].config(text=" ")
        labels[i].config(text=sol[pos-1][i])
    
def algorithm():
    """
    Run the A* algorithm
    """
    
    open_list.append(START)

    # A* Algorithm
    while len(open_list) > 0:
        # find the node with the minimum f value in the open list
        current = find_min()
        
        # add it to the closed list and remove it from the open list
        open_list.remove(current)
        closed_list.append(current)

        # if we are done, the finish
        if current == GOAL:
            execution_time = time() - START_TIME
            print("The puzzle was solved in ", configurations[current][1], " moves.")
            print("The "+HEURISTIC_TYPE+" heuristic was used, and the execution took "+str(execution_time)+" seconds.")
            break

        # for each child node
        for config in expand(current):
            
            # continue if the node is already closed
            if config in closed_list:
                continue
            
            # update the distance from the start node
            cost = configurations[current][1] + 1
            
            # if the new cost is better than the old cost, prepare it to be updated
            if config in open_list and cost < configurations[config][1]:
                open_list.remove(config)
            elif config in closed_list and cost < configurations[config][1]:
                closed_list.remove(config)
            
            # if it is in neither the open or closed list, add it to the open list, and update
            # the cost of getting to the node
            if config not in open_list and config not in closed_list:
                open_list.append(config)
                configurations[config][1] = cost
                configurations[config][2] = distance_heuristic(config)
                configurations[config][0] = configurations[config][1]+configurations[config][2]
                configurations[config][3] = current
                
                
def print_solution():
    print("Solution:\n")
    print("Start")
    for config in solution:
        for i in range(3):
            print(config[3*i], " ", config[3*i+1], " ", config[3*i+2])
        print("")
    print("Finish")
            
configurations = {
    START: [0, 0, distance_heuristic(START), None],
    GOAL: [0, 0, 0, None]
}

START_TIME = time()
algorithm()

# find the solution path
backtrack(GOAL)
solution.reverse()
print_solution()
