import networkx as nx

import random

def dfs(G, start, distance):
    """
    Calculate a route of a given distance in graph, G, using a basic Depth First Search algorithm.

    Parameters:
    -------
    G: networkx.Graph
        The graph object, derived from Open Street Maps (OSM) using osmnx methods
    start: int
        The starting vertex
    distance: float
        The target route distance

    Returns:
    -------
    route: list
        A list of vertices, represented as integers, defining the route.
    """
    # Check inputs
    if type(G) != nx.Graph:
        raise TypeError('G should be a networkx.Graph object')
    if type(start) != int:
        raise TypeError('start should be an integer, which represents the starting vertex')
    if not distance:
        raise TypeError('missing distance argument.')

    # route search algorithm...
    ## track 'visited' for each node in the Graph
    visited = {node:False for node in G.nodes}
    route = [start]
    d = 0 # distance traveled
    cur_node = route[-1]
    visited[cur_node] = True
    while d < distance:
        neighbors = list(G.neighbors(cur_node))
        deadend = True # check for deadends
        while neighbors:
            n = random.choice(neighbors)
            neighbors.remove(n)
            if not visited[n]:
                route.append(n)
                d += G[cur_node][n]['distance']
                cur_node = n
                visited[cur_node] = True
                deadend = False
                break
        if deadend:
            return route
    return route