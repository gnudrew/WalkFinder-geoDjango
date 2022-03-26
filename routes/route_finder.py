import networkx as nx
import random

def random_walk(G, v, dist=500):
    d = 0 # distance traveled
    path = [v] # starting point
    while d < dist:
        v = path[-1]
        neighbors = set(G[v].keys()) - set(path) # avoid nodes previously visited
        if len(neighbors)==0: # literal edge case --> no more untraversed nodes available.
            break
        print(f"  >> [random_walk] neighbors of {v}: {neighbors}")
        u = random.sample(neighbors,1)[0]
        path.append(u)
        d += G[v][u][0]['length']
    return (path, d)

def dfs(G, v_start, dist=500):
    """
    Calculate a route of a given distance in graph, G, using a basic Depth First Search algorithm.

    Parameters:
    -------
    G: networkx.Graph
        The graph object, derived from Open Street Maps (OSM) using osmnx methods
    v_start: int
        The starting vertex
    distance: float
        The target route distance

    Returns:
    -------
    route: list
        A list of vertices, represented as integers, defining the route.
    """
    # Check inputs
    if type(G) != nx.classes.multidigraph.MultiDiGraph:
        raise TypeError(f"G is type, {type(G)}, but should be type, networkx.Graph object")
    if type(v_start) != int:
        raise TypeError('start should be an integer, which represents the starting vertex')
    if not dist:
        raise TypeError('missing distance argument.')

    # route search algorithm...
    ## track 'visited' for each node in the Graph
    visited = {node:False for node in G.nodes}
    route = [v_start]
    branch_nodes = [] # define a branch_node as a node with 2 or more unvisited neighbors; we'll keep track of these as point to backtrack to in case we hit a deadend
    d = 0 # distance traveled
    print(route, f"d:{round(d)}/{round(dist)}")
    cur_node = route[-1]
    visited[cur_node] = True
    while d < dist:
    # Assume that the graph is large enough to always find at least one route greater than or equal to distance.
        neighbors = list(G.neighbors(cur_node))
        # check if cur_node is a branch_node
        unvisited_neighbors = [n for n in neighbors if not visited[n]]
        if len(unvisited_neighbors) >= 2: # the current node is a branch node if it has at least 2 unvisited neighbors; we can backtrack here upon hitting a deadend
            print(f"branch node at {cur_node} with {len(unvisited_neighbors)} unvisited neighbors: {unvisited_neighbors}")
            branch_nodes.append(cur_node)
        deadend = True # assume deadend until proven otherwise
        while neighbors:
            n = random.choice(neighbors)
            neighbors.remove(n)
            if not visited[n]:
                route.append(n)
                d += G[cur_node][n][0]['length']
                cur_node = n
                visited[cur_node] = True
                deadend = False
                # print route step
                print(route, f"d:{round(d)}/{round(dist)}")
                break
        if deadend:
            print(f"deadend at {cur_node}; branch_nodes.. {branch_nodes} ")
            # backtrack to previous branch_node
            prev_branch_node = branch_nodes.pop()
            while cur_node != prev_branch_node:
                prev_node = route.pop()
                cur_node = route[-1]
                d -= G[cur_node][prev_node][0]['length']
                # cur_node = prev_node
                print(route, f"d:{round(d)}/{round(dist)}")
    
    return (route, d)    
    
