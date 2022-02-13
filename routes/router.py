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

    return path