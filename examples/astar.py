import numpy as np

class Node:
    """A node class for A* pathfinding
       parent: parent of the current node
       position: position of the current node in the grid
       g is cost from start to current node
       h is heuristic based esstimated cost from the current node to the end node
       f is the total cost,  f = g + h"""

    def __init__(self, parent=None, position=None, dir_from_parent=None):
        self.parent = parent
        self.position = position
        self.dir_from_parent = dir_from_parent
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

    """
        This function returns the path of the current node from the start node    
    """

def get_child_dir(dir):
    number_dir = {
        1: "up",
        2: "left",
        -1: "down",
        -2: "right"
    }
    return number_dir.get(dir, "invalid direction")
def get_path(current_node, grid):
    print("get path called")
    path=[]
    direction = []
    no_rows, no_columns = np.shape(grid)
    result = [[ -1 for i in range(no_columns)] for j in range(no_rows)]
    current = current_node
    while current is not None:
        path.append(current.position)
        direction.append(current.dir_from_parent)
        current = current.parent
    #need to take inverse of the path as the path we built started fromt the goal ends to source.
    path_inv = path[::-1]
    direction.pop()
    direction = direction[::-1]

    start_value = 0
    for i in range(len(path)):
        result[path_inv[i][0]][path_inv[i][1]] = start_value
        start_value += 1
    print("returning from a star")
    return path, direction, result
    #return direction

def search(grid, cost, source, target):
    """
        Returns a list of tuples as a path from the given source to the given target in the given grid
    """
    print("source = ", source)
    print("target = ", target)
    start_node = Node(None, source)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, target)
    end_node.g = end_node.h = end_node.f = 0

    #Initialize two lists - one to keep track of what has been visited and another what to be visited

    to_be_visited = []
    visited = []

    #add the start node into the to be visited list
    to_be_visited.append(start_node)

    #the picar we will be working with can only visit one square left, right, up and down.
    move = [
        [-1, 0, 1], #up
        [0, -1, 2], #left
        [1, 0, -1], #down
        [0, 1, -2] #right
        ]
    
    no_rows, no_columns = np.shape(grid)

    while len(to_be_visited) > 0:
        #print("to_be_visited length = ", len(to_be_visited))
        current_node = to_be_visited[0]
        current_index = 0
        for index, item in enumerate(to_be_visited):
            if item.f < current_node.f:
                current_node = item
                current_index = index
        to_be_visited.pop(current_index)
        visited.append(current_node)
        if(current_node == end_node):
            return get_path(current_node, grid)

    #Find the children according to the move function

        children = []

        for new_position in move:
            node_position = (current_node.position[0] + new_position[0],
                            current_node.position[1] + new_position[1])

            ###This is to make sure that the movement happens within the range
            #
            # If border found jump to next children

            if(node_position[0] > (no_rows - 1) or 
                node_position[0] < 0 or
                node_position[1] > (no_columns - 1) or 
                node_position[1] < 0 ):
                continue
            #If any obstacles found, jump to next children

            if grid[node_position[0]][node_position[1]] != 0:
                continue

            #Create a new node and add to the children

            child = Node(current_node, node_position, new_position[2])
            children.append(child)
            #print("child = ", child.position)


        ## Iterate through all the children nodes

        for child in children:

            #if child is in the visited list, ignore that child.
            if len([visited_child for visited_child in visited if visited_child == child]) > 0:
                continue

            #populate the f,g,h values

            child.g = current_node.g + cost

            #Heurisitic costs calculated according to euclidian distance

            child.h = (((child.position[0] - end_node.position[0]) ** 2 ) -
                        ((child.position[1] - end_node.position[1]) ** 2 ))

            child.f = child.g + child.h

            #Add the child to the to be visited
            if len([open_node for open_node in to_be_visited if child == open_node and child.g > open_node.g]) > 0:
                continue

            to_be_visited.append(child)


def main():
    grid = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    start = [9,5]
    end = [0,0]
    cost = 1 
    path, direction, result = search(grid, cost, start, end)

    print(path)

    print('\n'.join([''.join(["{:" ">3d}".format(item) for item in row]) for row in path]))
    print(" \n")
    print('\n'.join([''.join(["{:" ">3d}".format(item) for item in row]) for row in result]))
    print("direction = ", direction)
    for i in direction:
        print("Next Direction = ", direction[i])

if __name__ == '__main__':
    main()



                





        