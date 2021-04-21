import pydot

graph = pydot.Dot('G', graph_type='digraph', bgcolor='grey')


initial_state = (
    (2, 8, 3),
    (1, 6, 4),
    (7, None, 5)
)

# initial_state =(
#     (1, 2, 3),
#     (7, 8, 4),
#     (None, 6, 5)
# )



goal_state = (
    (1, 2, 3),
    (8, None, 4),
    (7, 6, 5)
)

swappable_positions = {
    0: (1, 3),
    1: (0, 2, 4),
    2: (1, 5),
    3: (0, 4, 6),
    4: (1, 3, 5, 7),
    5: (2, 4, 8),
    6: (3, 7),
    7: (4, 6, 8),
    8: (5, 7)
}


def get_2d_pos_from_idx(idx):
    '''
    Return (row,col)
    '''
    return (idx//3, idx % 3)


def get_idx_from_2d_pos(row, col):
    '''
    Return idx
    '''
    return row*3+col


def swap(game_state, current_idx, swap_idx):
    '''
    Given the current  game state and  index, swap the empty value with swap state
    Eg: gamel_state =(
        (2,8,3),
        (1,6,4),
        (7,None,5)
    )
    current_idx = 7
    swap_idx = 8
    Result state = (
        (2,8,3),
        (1,6,4),
        (7,5,None)
    )
    '''
    curr_row, curr_col = get_2d_pos_from_idx(current_idx)
    swap_row, swap_col = get_2d_pos_from_idx(swap_idx)
    temp_state = []

    for i in game_state:
        row = []
        for j in i:
            row.append(j)
        temp_state.append(row)

    temp_state[curr_row][curr_col], temp_state[swap_row][swap_col] = temp_state[swap_row][swap_col], temp_state[curr_row][curr_col]

    new_state = []

    for i in temp_state:
        row = []
        for j in i:
            row.append(j)
        new_state.append(tuple(row))

    return tuple(new_state)


def get_empty_idx(game_state):
    idx = 0

    for i in game_state:
        for j in i:
            if j is None:
                # Found the index of empty space
                return idx
            else:
                idx += 1
    return idx



def move_BFS(visited: set, q: list = []):
    i = 1
    while len(q) > 0:

        # Find the empty position

        game_state, idx = q.pop(0)

        if game_state == goal_state:
            print("Found the goal..")
            pp(game_state)
    
            return True

        # Find the all possible move for that state
        positions = swappable_positions[idx]

        for position in positions:

            new_state = swap(game_state, idx, position)
            if new_state in visited:
                continue
            else:
                
                node = pydot.Node(str(new_state),label=str(new_state)+' '+str(i) )
                node.set_style("filled")
                node.set_fillcolor('white')
                node.set_fontcolor("black")

                graph.add_node(node)
                edge = pydot.Edge(str(game_state),str(new_state))
                graph.add_edge(edge)

                visited.add(new_state)

                # pp(new_state)
                empty_idx = get_empty_idx(new_state)

                q.append((new_state, empty_idx))
                i += 1
    
    print("Goal Not found")
    return False




def move_DFS(visited: set, stack: list = [],max_depth=10):
    i = 1
    while len(stack) > 0:

        # Find the empty position

        game_state, idx, depth = stack.pop()
        # print(game_state,idx,depth)
        
        if game_state == goal_state:
            print("Found the goal..")
            pp(game_state)
        
            return True
        
        if depth > max_depth:
            continue

        # Find the all possible move for that state
        positions = swappable_positions[idx]
        

        for position in positions:

            new_state = swap(game_state, idx, position)
            if new_state in visited:
                continue
            else:
                node = pydot.Node(str(new_state),label=str(new_state)+' '+str(i) )
                node.set_style("filled")
                node.set_fillcolor('white')
                node.set_fontcolor("black")

                graph.add_node(node)
                edge = pydot.Edge(str(game_state),str(new_state))
                graph.add_edge(edge)

                visited.add(new_state)

                empty_idx = get_empty_idx(new_state)

                stack.append((new_state, empty_idx,depth+1))
                i += 1
    
    print("Goal Not found")
    return False


def pp(list_2d, end='\n'):
    if end == '\n':
        print('-------------------------')
    for i in list_2d:
        for j in i:
            print(j, end=' ')
        print()
    if end == '\n':
        print('-------------------------')


if __name__ == "__main__":

    visited = set()
    visited.add(initial_state)

    idx = get_empty_idx(initial_state)
    # q = [(initial_state, idx)]
    stack = [(initial_state, idx,0)]

    node = pydot.Node(str(initial_state),label=str(initial_state)+' 0')
    node.set_style("filled")
    node.set_fillcolor('yellow')
    node.set_fontcolor("black")
    graph.add_node(node)

    print("Initial State:", initial_state)
    # res = move_BFS(visited, q)
    res =  move_DFS(visited, stack)


    print("Drawing State Space...")
    print("Total Nodes:", len(graph.get_nodes()))
    if res:
        node = graph.get_node(f'"{str(initial_state)}"')[0]
        node.set_style("filled")
        node.set_fillcolor('yellow')

        node = graph.get_node(f'"{str(goal_state)}"')[0]
        node.set_style("filled")
        node.set_fillcolor('red')
    

    graph.write_png('output_dfs_10.png',prog='dot')
    print("Saved state space as output.png.")

