from math import inf, sqrt
from tkinter import*

class Astar:
    
    def __init__(self, heuristic_type, start, goal):
        self.heuristic_type = heuristic_type
        self.start = start
        self.goal = goal
        self.open_list = []
        self.closed_list = []
        self.solution = []
        self.configurations = {
            self.start: [0,0,self.distance_heuristic(self.start), None]
        }
            

    def distance_heuristic(self, node):
        """ 
        calculates the distance heuristic (h-value) for a given node
        
        parameters:
        - node: a 9-tuple containing the board information for a configuration
        """
        
        position = {
            self.goal[0]: (0,0),
            self.goal[1]: (0,1),
            self.goal[2]: (0,2),
            self.goal[3]: (1,0),
            self.goal[4]: (1,1),
            self.goal[5]: (1,2),
            self.goal[6]: (2,0),
            self.goal[7]: (2,1),
            self.goal[8]: (2,2)
        }
        
        if self.heuristic_type == "absolute":
            # calculate the straight line distance that a tile needs
            # to travel to be in the correct place

            # find the distance between each node and its intended position
            # and add it to the total
            total = 0
            for i in range(9):
                goal_position = position[node[i]]
                actual_position = position[i]
                total += sqrt((goal_position[0]-actual_position[0])**2+(goal_position[1]-actual_position[1])**2)

            return total

        elif self.heuristic_type == "manhattan":
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
                total += abs(goal_position[0]-actual_position[0])+abs(goal_position[1]-actual_position[1])

            return total


    def find_min(self):
        """
        find the node with the minimum f value in the open list
        """
        minimum = inf
        min_node = None
        for node in self.open_list:
            if self.configurations[node][0] < minimum:
                minimum = self.configurations[node][0]
                min_node = node
        return min_node


    def child(self, swap, node, blank_index):
        
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
        h = self.distance_heuristic(new_config)
        
        # if the new configuration (after the swap) is already exisiting,
        # update it's h value, otherwise create a new entry.
        if new_config in self.configurations.keys():
            self.configurations[new_config] = [self.configurations[new_config][0]+h, 0, h, self.configurations[new_config][3]]
        else:
            self.configurations[new_config] = [h, 0, h, None]

        return new_config

    def expand(self, node):
        """
        expand a node, and return its children
        
        parameters:
        - node: the configuration to expand
        """
        
        # a dictionary of the possible moves that can be made depending on where the blank space is
        swaps = {
            0: [1,3],
            1: [0,2,4],
            2: [1,5],
            3: [0,4,6],
            4: [1,3,5,7],
            5: [2,4,8],
            6: [3,7],
            7: [4,6,8],
            8: [5,7]
        }

        # for each possible move, make the move and add the result to the list
        children = []

        blank_index = node.index(0)
        for swap in swaps[blank_index]:
            new_child = self.child(swap, node, blank_index)
            if new_child in self.configurations.keys():
                children.append(new_child)

        return children


    def backtrack(self, current):
        """ 
        recursively find the solution path by looking through the parents of each child
        """
        if current == None:
            return
        self.solution.append(current)
        self.backtrack(self.configurations[current][3])
        
        
    def next_stage(self, labels):
        """
        display the next configuration in the solution path
        
        parameters:
        - labels: the labels to display the numbers on
        - sol: the solution path
        """
        
        sol = self.solution
        
        config = tuple([int(label["text"]) for label in labels[:9]])
        pos = sol.index(config)

        if config == self.goal:
            labels[9].config(text="Finish")
            return
        elif sol[pos+1] == self.goal:
            labels[9].config(text="Finish")
        else:
            labels[9].config(text="")
            
        for i in range(9):
            labels[i].config(text = sol[pos+1][i])
            
    def prev_stage(self, labels):
        """
        display the previous configuration in the solution path
        
        parameters:
        - labels: the labels to display the numbers on
        - sol: the solution path
        """
        
        sol = self.solution
        
        config = tuple([int(label["text"]) for label in labels[:9]])
        pos = sol.index(config)
        
        if config == self.start or sol[pos-1] == self.start:
            labels[9].config(text="Start")
            return
        else:
            labels[9].config(text="")
            
        for i in range(9):
            labels[i].config(text = sol[pos-1][i])
        

    def algorithm(self):
        """
        A* Algorithm
        """
        
        self.open_list.append(self.start)


        # A* Algorithm
        while len(self.open_list) > 0:
            
            # find the node with the minimum f value in the open list
            current = self.find_min()
            
            # add it to the closed list and remove it from the open list
            self.open_list.remove(current)
            self.closed_list.append(current)

            # if we are done, the finish
            if current == self.goal:
                break

            # for each child node
            for config in self.expand(current):
                
                # continue if the node is already closed
                if config in self.closed_list:
                    continue
                
                # update the distance from the start node
                cost = self.configurations[current][1] + 1
                
                # if the new cost is better than the old cost, prepare it to be updated
                if config in self.open_list and cost < self.configurations[config][1]:
                    self.open_list.remove(config)
                elif config in self.closed_list and cost < self.configurations[config][1]:
                    self.closed_list.remove(config)
                
                # if it is in neither the open or closed list, add it to the open list, and update
                # the cost of getting to the node
                if config not in self.open_list and config not in self.closed_list:
                    self.open_list.append(config)
                    self.configurations[config][1] = cost
                    self.configurations[config][2] = self.distance_heuristic(config)
                    self.configurations[config][0] = self.configurations[config][1]+self.configurations[config][2]
                    self.configurations[config][3] = current


        # find the solution path
        self.backtrack(self.goal)
        self.solution.reverse()
        
def count_inversions(start_tuple):
    """
    Count the number of inversions required to solve the configuration
    """
    
    swap_count = 0
    for i in range(9):
        for j in range(i+1,9):
            if start_tuple[i] < start_tuple[j]:
                swap_count += 1
                
    return swap_count
        
def check_valid(start_tuple, goal_tuple):
    """
    Check whether a given state is valid, and solvable
    """
    
    # if the tuple is not valid
    if set(start_tuple) != set([0, 1, 2, 3, 4, 5, 6, 7, 8]) or set(goal_tuple) != set([0, 1, 2, 3, 4, 5, 6, 7, 8]):
        return [False, "invalid"]
    
    elif len(start_tuple) != 9 or len(goal_tuple) != 9:
        return [False, "invalid"]    
    
    # check whether the parity of the start and goal are acceptable
    swap_count_start = count_inversions(start_tuple)
    swap_count_goal = count_inversions(goal_tuple) 
       
    if swap_count_start%2 != swap_count_goal%2:
        return [False, "parity"]
    
    return [True, None]

def reset_gui(error_label, standard_solve_yes, standard_solve_no):
    """
    Reset the GUI
    """
    
    error_label.config(text="")
    standard_solve_no.destroy()
    standard_solve_yes.destroy()
    
def start_standard_algorithm(start_button, manhattan_pick, absolute_pick, start_entry, start_tuple, goal_tuple, heuristic_type, goal_entry, error_label, standard_solve_no, standard_solve_yes):
    """
    Start the A* Algorithm with a standard configuration
    """
    
    # start the algorithm
    astar = Astar(heuristic_type.get(), start_tuple, goal_tuple)
    astar.algorithm()
    
    # clear the GUI
    start_button.destroy()
    start_entry.destroy()
    manhattan_pick.destroy()
    absolute_pick.destroy()
    error_label.destroy()
    standard_solve_no.destroy()
    standard_solve_yes.destroy()
    goal_entry.destroy()
    
    labels = []
    
    #display the solution in a GUI
    top_label = Label(root, text="Start")
    top_label.grid(column=0, row=0, columnspan=3)

    for i in range(3):
        for j in range(3):
            b = Button(root, text=astar.start[3*i+j])
            b.grid(row=i+1, column=j)
            labels.append(b)
    labels.append(top_label)
            
    next_button = Button(root, text="Next", command=lambda: astar.next_stage(labels))
    next_button.grid(row=1, column=4)
    prev_button = Button(root, text="Prev", command=lambda: astar.prev_stage(labels))  
    prev_button.grid(row=2, column=4) 
       
def start_algorithm(start_button, manhattan_pick, absolute_pick, start_entry, heuristic_type, goal_entry, error_label):
    """
    Start the A* algorithm, if an invalid start or goal is given, reject it. If an unsolvable solution is given, give the
    user the option to solve it to a standard goal state.
    """
    
    start_tuple = tuple([int(i) for i in start_entry.get()])
    goal_tuple = tuple([int(i) for i in goal_entry.get()])
    
    # check whether the solution is valid and solvable
    validity = check_valid(start_tuple, goal_tuple)
    if not validity[0]:
        if validity[1] == "invalid":
            # reject if invalid
            error_label.config(text = "This configuration is not valid. Please enter a valid configuration")
            return
        else:
            # offer to solve to a standard goal state if unsolvable
            error_label.config(text = "This configuration is not solvable. Would you like to solve to a standard configuration?")
            if check_valid(start_tuple, (0, 1, 2, 3, 4, 5, 6, 7, 8))[0]:
                standard_goal = (0, 1, 2, 3, 4, 5, 6, 7, 8)
            else:
                standard_goal = (1, 2, 3, 8, 0, 4, 7, 6, 5)
            standard_solve_yes = Button(root, text="Yes")
            standard_solve_yes.grid(row=6, column=0)
            standard_solve_no = Button(root, text="No")
            standard_solve_no.grid(row=6, column=1)
            
            standard_solve_no.config(command = lambda: reset_gui(error_label, standard_solve_yes, standard_solve_no))
            standard_solve_yes.config(command = lambda: start_standard_algorithm(start_button, manhattan_pick, absolute_pick, start_entry, start_tuple, standard_goal, heuristic_type, goal_entry, error_label, standard_solve_no, standard_solve_yes))
    else:
        # if it is valid, run the algorithm and clear the GUI
        astar = Astar(heuristic_type.get(), start_tuple, goal_tuple)
        astar.algorithm()
        
        start_button.destroy()
        start_entry.destroy()
        manhattan_pick.destroy()
        absolute_pick.destroy()
        error_label.destroy()
        goal_entry.destroy()
        
        labels = []
        
        #display the solution in a GUI
        top_label = Label(root, text="Start")
        top_label.grid(column=0, row=0, columnspan=3)

        for i in range(3):
            for j in range(3):
                b = Button(root, text=astar.start[3*i+j])
                b.grid(row=i+1, column=j)
                labels.append(b)
        labels.append(top_label)
                
        next_button = Button(root, text="Next", command=lambda: astar.next_stage(labels))
        next_button.grid(row=1, column=4)
        prev_button = Button(root, text="Prev", command=lambda: astar.prev_stage(labels))  
        prev_button.grid(row=2, column=4) 
 
        
# set up the GUI
root = Tk()

start_entry = Entry(root, text="Starting Configuration")
start_entry.grid(row=0, column=0)
goal_entry = Entry(root, text="Goal Configuration")
goal_entry.grid(row=1, column=0)

heuristic_type = StringVar()
heuristic_type.set("manhattan")
manhattan_pick = Radiobutton(root, text="Manhattan", variable=heuristic_type, value="manhattan")
manhattan_pick.grid(row=2, column=0)
absolute_pick = Radiobutton(root, text="Euclidean", variable=heuristic_type, value="absolute")
absolute_pick.grid(row=3, column=0)

error_label = Label(root, text="", fg="red")
error_label.grid(row=5, column=0, columnspan=5)

start_button = Button(root, text="Start", command=lambda: start_algorithm(start_button, manhattan_pick, absolute_pick,
                                                                          start_entry, heuristic_type, goal_entry,
                                                                          error_label))
start_button.grid(row=4, column=0)


root.mainloop()