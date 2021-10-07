These are the required code files for the ECM2423 Coursework. I have provided an explanation of how to use each file.

(1.1) astar.py:
    This program finds the solution to a specific case of the 8-puzzle, namely solving 
    7 2 4    0 1 2
    5 0 6 to 3 4 5
    8 3 1    6 7 8
    Where 0 represents the blank tile. 
    In order to change the distance heuristic the algorithm uses, change the variable 'heuristic_type' to either "manhattan" or "euclidean".
    If any other string is used, the code will default to a heuristic of 0, which is trivially admissible.

(1.3) astar_generic.py:
    This program will find the solution to a general case of the 8-puzzle.
    To use it, input the start state into the top box of the GUI, for example if your start state is
    0 7 2
    4 5 6
    8 3 1
    Then input '072456831'.
    Repeat with the intended goal state in the second box in the GUI. If either input is invalid, or unsolvable, the program will notify you,
    and in the latter case you will be asked if you want the program to solve to a standard solution. For an even parity, this will be
    '012345678', and for an odd parity this will be '123804765'.


(2.1)
    In this script, you can change the 'display' variable to "centroids", "clusters", or "accuracy". These will produce
    a representation of the centroids, the clusters the program makes, or the accuracy of the program over different amounts of training data
    respectively.
    You can also change the 'centroid-type' variable to 'random' to make the initial centroids random, but this may make the results much worse.

(3)
    This script will run a decision tree on the data, and produce a graph of its accuracy of prediction with varying depth.