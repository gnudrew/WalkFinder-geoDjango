from django.shortcuts import render
from django.http import HttpResponse

from .buildmap import buildmap_start, buildmap_route
from random import random as r # interval r() -> x in [0,1)
import osmnx as ox
from networkx.readwrite import json_graph
graph_write = json_graph.adjacency_data
graph_read = json_graph.adjacency_graph


# Create your views here.
def home_view(request):
    # return HttpResponse("<h1>Hello World!</h1>")
    # print(request)
    # print(render(request, "base.html"))

    # request.session['fav_color']='red'
    # print('Home_View session: fav_color is:', request.session['fav_color'])

    return render(request, "base.html", {})

def mapgen_view(request):
    if request.method=='POST':
        # get form inputs
        lat = float(request.POST.get('lat'))
        lon = float(request.POST.get('lon'))
        # store to session
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
        # m is the folium map from the previous call of mapgen_view().
        # for now, I'll regenerate it with hard-coded location.
        # Later, I'll probably store either the map object, or the details needed to regenerate it in the database
        # ... like under some "Previous Map" location in memory.

        # retrieve session inputs
        lat = request.session['lat']
        lon = request.session['lon']
        # build map
        m = buildmap_start(lat,lon)

        return render(request, "routegen.html", {'folium_map':m._repr_html_()})

    if request.method=='POST':
        # get form input
        target_time = int(request.POST.get('target_time'))

        # print("~=~== FRESH AFTER POST: time TYPE is...", type(target_time))

        # store to session
        request.session['target_time'] = target_time

        # m is the folium map from the previous call of mapgen_view() or routegen_view().
        # regenerate it for now with hard-coded coordinates
        # Later, I'll probably store either the map object, or the details needed to regenerate it in the database
        # ... like under some "Previous Map" location in memory.

        # retrieve map inputs from session
        lat = float(request.session['lat'])
        print('LAT is',lat,'with type',type(lat))
        lon = float(request.session['lon'])

        
        # Build Graph of surrounding walking network. Assume we will walk out then back, so dist=d/2
        speed_meters_per_min = 3*(1609.)/60
        distance = speed_meters_per_min * target_time
        print("target_time TYPE  is:", type(target_time))
        print("speed_meters_per_min TYPE is:", type(speed_meters_per_min))
        print("target time: ", target_time, "minutes")
        print("distance", distance, "meters")
        G = ox.graph_from_point((lat,lon), network_type="walk", dist=distance/2, dist_type="network")
        # store G to session
        # request.session['G'] = graph_write(G)
          ## Currently cannot write graphs because type <'Linestring'> is not JSON serializable...

        # Random End Point: randomly generate lat and lon
        # rand_lat = (lat-.004) + .008*r()
        # rand_lon = (lon-.008) + .016*r()

        # get node id's from G
        node_ids = [node for node in G.nodes]
        # randomly choose one
        number_of_nodes = len(node_ids)
        chosen_one = int(r()*(number_of_nodes)) # int() conversion truncates, never rounds up
        # get lat and lon
        rand_lat = G.nodes[node_ids[chosen_one]]['y']
        rand_lon = G.nodes[node_ids[chosen_one]]['x']
        # store to session
        request.session['rand_lat'] = rand_lat
        request.session['rand_lon'] = rand_lon

        # Build Route path (list of nodes) from (lat, lon) to (rand_lat, rand_lon)
        # Find nearest node to homebase coordinates
        nn = ox.distance.nearest_nodes(G, lon, lat) # nearest node
        # if len(nn) > 1:
        #     nn = nn[0]
        route = ox.distance.shortest_path(G, nn, node_ids[chosen_one])

        # build map
        m = buildmap_start(lat, lon)
        m = buildmap_route(m, target_time, (lat, lon), (rand_lat, rand_lon), G=G, route=route)
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