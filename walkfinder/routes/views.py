from django.shortcuts import render
from .models import Mapgens
from .buildmap import buildmap_start, buildmap_route

from django.contrib.gis.geos import Point
from random import random as r # interval r() -> x in [0,1)
import osmnx as ox
from networkx import NetworkXPointlessConcept
from networkx.readwrite import json_graph
graph_write = json_graph.adjacency_data
graph_read = json_graph.adjacency_graph


# Create your views here.
def home_view(request):
    return render(request, "base.html", {})

def mapgen_view(request):
    if request.method=='POST':
        # get form inputs
        lat = float(request.POST.get('lat'))
        lon = float(request.POST.get('lon'))
        # store these to session
        request.session['lat'] = lat
        request.session['lon'] = lon
        # server-side print
        print('======== mapgen_view ========')
        print("(lat,lon) = ",str((lat,lon)))
        print('====== END mapgen_view ======')
        # build map
        m = buildmap_start(lat, lon)

        return render(request, "mapgen.html", 
            {
                'lat':lat, 
                'lon':lon, 
                'folium_map':m._repr_html_(),
            })
    
    if request.method=='GET':
        # Change this to URL routing: If user submits GET request manually at URL `/mapgen/` redirect to URL `/`.
        return render(request,"base.html")

def routegen_view(request):
    if request.method=='GET':
        # retrieve session inputs
        lat = request.session['lat']
        lon = request.session['lon']
        # rebuild map
        m = buildmap_start(lat,lon)

        return render(request, "routegen.html", 
        {
            'folium_map':m._repr_html_()
        })

    if request.method=='POST':
        # get form input
        target_time = int(request.POST.get('target_time'))
        # print("~=~== FRESH AFTER POST: time TYPE is...", type(target_time))

        # store this to session
        request.session['target_time'] = target_time

        # retrieve map inputs from session
        lat = float(request.session['lat'])
        lon = float(request.session['lon'])
        
        # Build Graph of surrounding walking network. Assume we will walk out then back, so dist=d/2
        speed_meters_per_min = 3*(1609.)/60
        distance = speed_meters_per_min * target_time
    
        try: # got ValueError "found no graph nodes within the requested polygon"
            G = ox.graph_from_point((lat,lon), network_type="walk", dist=distance/2, dist_type="network")
        except (ValueError, NetworkXPointlessConcept) as err:
            print(err)
            # rebuild map
            m = buildmap_start(lat, lon)
            # Build error html
            except_html = "<h1>Processing Error occured</h1><p>No walking nodes found in search radius. Either you're out in the boonies or your target time is too small. Please adjust your inputs and try again.<p>"
            return render(request, "routegen.html", 
            {
                'folium_map':m._repr_html_(), 
                'except_html':except_html,
                'target_time':target_time, 
                # 'number_of_nodes':number_of_nodes,
                # 'rand_lat':rand_lat,
                # 'rand_lon':rand_lon,                
            })

        # store G to session
        # request.session['G'] = graph_write(G)
          ## Currently cannot write graphs because type <'Linestring'> is not JSON serializable...

        # get node id's from G
        node_ids = [node for node in G.nodes]
        # randomly choose a node
        number_of_nodes = len(node_ids)
        chosen_one = int(r()*(number_of_nodes)) # int() conversion truncates, never rounds up
        # get lat and lon from this node
        rand_lat = G.nodes[node_ids[chosen_one]]['y']
        rand_lon = G.nodes[node_ids[chosen_one]]['x']
        # store these to session
        request.session['rand_lat'] = rand_lat
        request.session['rand_lon'] = rand_lon

        # Find nearest node to homebase coordinates
        nn = ox.distance.nearest_nodes(G, lon, lat)
        nn_lat = G.nodes[nn]['y']
        nn_lon = G.nodes[nn]['x']

        # Find route, a list of nodes, from start to end
        route = ox.distance.shortest_path(G, nn, node_ids[chosen_one])

        # build map from these inputs
        m = buildmap_start(lat, lon)
        try: # got ValueError : "graph contains no edges"
            m = buildmap_route(m, target_time, (lat, lon), (rand_lat, rand_lon), G=G, route=route)
        except ValueError as err: # likely graph has no edges
            print(err)
            # rebuild map
            m = buildmap_start(lat, lon)
            # exception html
            except_html = "<h1>Processing Error Occured</h1><p>We found a valid start node, but the walking network within your inputs is too small. Please increase your target time or relocate and try again.<p>"

            return render(request, "routegen.html", 
            {
                'folium_map':m._repr_html_(), 
                'except_html':except_html,
                'target_time':target_time, 
                'number_of_nodes':number_of_nodes,
                'rand_lat':rand_lat,
                'rand_lon':rand_lon,                
            })

        # Save inputs to db
        Mapgens.objects.create(
            home_loc = Point(y=lat,x=lon),
            start_loc = Point(y=nn_lat,x=nn_lon),
            end_loc = Point(y=rand_lat,x=rand_lon),
            target_time = target_time,
            speed_mph = 3,
            speed_mpm = speed_meters_per_min,
            dist = distance/2,
            dist_type = "network",
            network_type = "walk",
        )

        return render(request, "routegen.html", 
        {
            'target_time':target_time, 
            'folium_map':m._repr_html_(), 
            'number_of_nodes':number_of_nodes,
            'rand_lat':rand_lat,
            'rand_lon':rand_lon,
        })

def walk_view(request):
    # retrieve map inputs from session
    lat = request.session['lat']
    lon = request.session['lon']
    rand_lat = request.session['rand_lat']
    rand_lon = request.session['rand_lon']
    target_time = request.session['target_time']
    # G = graph_read(request.session['G'])

    m = buildmap_start(lat, lon)
    m = buildmap_route(m, target_time, (lat, lon), (rand_lat, rand_lon))
    
    return render(request, "walk.html", 
    {
        'folium_map':m._repr_html_(), 
        'lat':lat,
        'lon':lon,
        'rand_lat':rand_lat,
        'rand_lon':rand_lon,
        'target_time':target_time,
    })