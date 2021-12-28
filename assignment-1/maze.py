import numpy as np

# This class is to represent node's position, its parent and values such as:
# g - cost of moving from start node to current node
# h - heuristic value
# f - g + h

class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0
    def __eq__(self, other):
        return self.position == other.position

def return_path(current_node,maze):
    path = [] # This list stores the path if there exists any
    no_rows, no_columns = np.shape(maze)
    result = [[-1 for i in range(no_columns)] for j in range(no_rows)] # We initialize every node's value to -1
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    path = path[::-1]
    start_value = 0
    for i in range(len(path)):
        result[path[i][0]][path[i][1]] = start_value
        start_value += 1
    return result


def search(maze, cost, start, end):
    
    # Here we initialize start and end nodes along with its g,h,f values
    start_node = Node(None, tuple(start))
    end_node = Node(None, tuple(end))
    start_node.g = start_node.h = start_node.f = 0
    end_node.g = end_node.h = end_node.f = 0

    open_list = []  
    closed_list = [] 

    open_list.append(start_node)
    outer_iterations = 0
    max_iterations = (len(maze) // 2) ** 10 # This variable makes sure that we don't run into infinite loop iterations

    move  =  [[-1, 0 ], # go up
              [ 0, -1], # go left
              [ 1, 0 ], # go down
              [ 0, 1 ]] # go right

    no_rows, no_columns = np.shape(maze)
    
    while len(open_list) > 0:

        # Here we loop until open list becomes empty. That is we expand all the nodes present in open list
        
        outer_iterations += 1    
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        if outer_iterations > max_iterations:
            print ("Exiting the search as number of iterations taken is greater than maximum possible iterations")
            return return_path(current_node,maze)

        open_list.pop(current_index) # Here we are popping the node after it is expanded
        closed_list.append(current_node) # And we add it to closed list

        if current_node == end_node:
            return return_path(current_node,maze)

        children = []

        for new_position in move: 

            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            if (node_position[0] > (no_rows - 1) or 
                node_position[0] < 0 or 
                node_position[1] > (no_columns -1) or 
                node_position[1] < 0):
                continue

            if maze[node_position[0]][node_position[1]] != 0:
                continue

            new_node = Node(current_node, node_position)

            children.append(new_node)

        for child in children:

            if len([visited_child for visited_child in closed_list if visited_child == child]) > 0:
                continue

            child.g = current_node.g + cost
            # Calculating euclidean distance for heuristic value
            child.h = (((child.position[0] - end_node.position[0]) ** 2) + 
                       ((child.position[1] - end_node.position[1]) ** 2)) 

            child.f = child.g + child.h # Calculating f value
            if len([i for i in open_list if child == i and child.g > i.g]) > 0:
                continue

            open_list.append(child)


if __name__ == '__main__':

    maze = [[0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 1, 0, 1, 0, 0],
            [0, 1, 0, 0, 1, 0],
            [0, 0, 0, 0, 1, 0],
            [0, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 1, 0]]
    
    start = [0, 0] # starting position
    end = [6,5] # ending position
    cost = 1 # cost per movement

    path = search(maze,cost, start, end)
    #print(path)
    print('\n'.join([''.join(["{:" ">3d}".format(item) for item in row]) 
      for row in path]))
