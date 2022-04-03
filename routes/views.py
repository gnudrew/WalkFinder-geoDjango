from django.conf import settings
import os, json

from django.shortcuts import render, redirect
from .models import Mapgens
from .buildmap import buildmap_base, buildmap_route
from utils.transformations import ll_to_json

from django.contrib.gis.geos import Point
from random import random as r # interval r() -> x in [0,1)
import osmnx as ox
from networkx import NetworkXPointlessConcept
from osmnx.io import load_graphml, save_graphml

from .route_finder import random_walk, dfs

# Create your views here.
def home_view(request):
    context = {
        'is_POST_request':0,
    }
    return render(request, "base.html", context)

def mapgen_view(request):
    if request.method=='POST':
        # get form inputs
        lat = float(request.POST.get('lat'))
        lon = float(request.POST.get('lon'))
        # store these to session
        request.session['lat'] = lat
        request.session['lon'] = lon
        # server-side print
        # print('======== mapgen_view ========')
        # print("(lat,lon) = ",str((lat,lon)))
        # print('====== END mapgen_view ======')
        # build map
        m = buildmap_base(lat, lon)

        context = {
            'is_POST_request':1,
            'lat':lat, 
            'lon':lon, 
            'folium_map':m._repr_html_(),            
        }
        return render(request, "mapgen.html", context)
    
    if request.method=='GET':
        # Change this to URL routing: If user submits GET request manually at URL `/mapgen/` redirect to URL `/`.
        context = {
            'is_POST_request':0,
        }
        return render(request,"base.html",context)

def sanitize_location_inp():
    pass

def get_graph_filepath():
    base_dir = settings.BASE_DIR
    save_dir = os.path.join(base_dir, "data")
    filepath = os.path.join(save_dir, "G.graphml") # use 1 file for PoC
    return filepath

def routegen_view(request):
    if request.method=='GET':
        # retrieve session inputs, or default if first call
        lat = request.session.get('lat', "")
        lon = request.session.get('lon', "")
        target_time = request.session.get('target_time',"")
        # rebuild map
        m = buildmap_base(lat,lon)

        context = {
            'folium_map':m._repr_html_(),
            'is_POST_request':0,
            'target_time':target_time,
        }
        return render(request, "routegen.html", context)

    if request.method=='POST':
        print("Retrieving Stuff...")
        ## Retrieve form input
        target_time = int(request.POST.get('target_time'))
        is_new_time = int(request.POST.get('is_new_time')) #1=True,0=False
        is_first_request = int(request.POST.get('is_first_request'))

        # store this to session
        request.session['target_time'] = target_time

        # retrieve map inputs from session
        lat = float(request.session['lat'])
        lon = float(request.session['lon'])
        
        ## Generate new graph if time changed, else load previous graph from memory
        # constants
        speed_miles_per_hour = 3
        speed_meters_per_min = speed_miles_per_hour * 26.8224 # unit conversion
          ## TASK --> build functionality to track user average walking speed and load this from database each time a user requests a new route.
        distance = speed_meters_per_min * target_time
        if is_new_time or is_first_request:
            # Build Graph of surrounding walking network. Assume we will walk out then back, so dist=d/2
            is_first_request = 0
            context = {
                    'is_first_request':0,
                    'is_POST_request':1,
                    'target_time':target_time,              
            }
            print("Querying OSM API for new Graph...")
            try: # got ValueError "found no graph nodes within the requested polygon"
                G = ox.graph_from_point((lat,lon), network_type="walk", dist=distance/2*1.25, dist_type="network")
            except (ValueError, NetworkXPointlessConcept) as err:
                print("EXCEPTED:", type(err), "; MESSAGE:", err)
                # rebuild map
                m = buildmap_base(lat, lon)
                # Build error html
                except_html = "<div style='border:4px solid Tomato;'><h3>Processing Error</h3><p>No walking nodes found in search radius. Either you're way out in the Boonies or your target time is too small. Please adjust your inputs and try again.</p></div>"
                context['except_html'] = except_html
                context['folium_map'] = m._repr_html_()
                return render(request, "routegen.html", context)
            except:
                print("EXCEPTED: unkown; MESSAGE: Try: call of ox.graph_from_point() in routegen_view()")
                
                # rebuild map
                m = buildmap_base(lat, lon)
                # exception html
                except_html = "<div style='border:4px solid Tomato;'><h3>Processing Error</h3><p>An unknown error occured. Please ask a Dev to consult the server logs and try again.</p></div>"
                context['except_html'] = except_html
                context['folium_map'] = m._repr_html_()
                return render(request, "routegen.html", context)

            # store G to file
            print("Saving Graph to memory...")
            save_graphml(G, filepath=get_graph_filepath())
        else:
            # load previous graph
            print("Loading Graph from memory...")
            G = load_graphml(filepath=get_graph_filepath())

        print("Finding node nearest homebase coordinates...")
        # Find nearest node to homebase coordinates
        nn = ox.distance.nearest_nodes(G, lon, lat)
        nn_lat = G.nodes[nn]['y']
        nn_lon = G.nodes[nn]['x']
        print(f" >> lat: {lat}->{nn_lat}; lon: {nn_lon}->{nn_lon}")

        ## Calculate a Random Route from home
        print("Calculating a random route...")
        # Manually set method for now...
        method = 2
        if method == 0:
        # fastest path to randomly selected node in full Graph
            print(" >> [Method 0] Selecting destination point from entire graph...")
            # get node id's from G
            node_ids = list(G.nodes)
            # randomly choose a node
            number_of_nodes = len(node_ids)
            chosen_one = int(r()*(number_of_nodes)) # int() conversion truncates, never rounds up

            print(" >> [Method 0] Getting lat/lon from destination point...")
            # get lat and lon from this node
            rand_lat = G.nodes[node_ids[chosen_one]]['y']
            rand_lon = G.nodes[node_ids[chosen_one]]['x']
            # store these to session
            request.session['rand_lat'] = rand_lat
            request.session['rand_lon'] = rand_lon

            print(" >> [Method 0] Calculating fastest route from home node to destination node")
            # Find route, a list of nodes, from start to end
            route = ox.distance.shortest_path(G, nn, node_ids[chosen_one])
            print(f"route of type {type(route)}:")
            print(route)
            # Store route to session
            request.session['route'] = route
        elif method == 1:
        # random walk of target distance starting at home 
            print(" >> [Method 1] Calculating route via random walk from home node...")
            route, route_distance = random_walk(G, nn, dist=distance/2)
            print(f"route of type {type(route)}:")
            print(route)
            # store route to session
            request.session['route'] = route
            # get lat and lon of final node in route and store to session
            print(" >> [Method 1] Getting lat/lon of final node in the route")
            rand_lat = G.nodes[route[-1]]['y']
            rand_lon = G.nodes[route[-1]]['x']
            request.session['rand_lat'] = rand_lat
            request.session['rand_lon'] = rand_lon
        elif method == 2:
        # basic dfs until target distance is acheived
            print(" >> [Method 2] Calculating route via dfs...")
            try:
                route, route_distance = dfs(G, nn, dist=distance/2) # half round trip
                route_distance *= 2 # convert to round trip
                routegen_exception = ''
            except Exception as e:
                route, route_distance = [], 0
                routegen_exception = e
            print(f"route of type {type(route)}:")
            print(route)
            # store route to session
            request.session['route'] = route
            # get lat and lon of final node in route and store to session
            print(" >> [Method 1] Getting lat/lon of final node in the route")
            rand_lat = G.nodes[route[-1]]['y']
            rand_lon = G.nodes[route[-1]]['x']
            request.session['rand_lat'] = rand_lat
            request.session['rand_lon'] = rand_lon

        # build map from these inputs
        print("Building a new Map...")
        m = buildmap_base(lat, lon)
        number_of_nodes = len(list(G.nodes))
        try: # got ValueError : "graph contains no edges"
            m = buildmap_route(m, target_time, (lat, lon), (rand_lat, rand_lon), G=G, route=route)
        except ValueError as err: # likely graph has no edges
            print("EXCEPTED:", type(err), "; MESSAGE:", err)
            # rebuild map
            m = buildmap_base(lat, lon)
            # exception html
            except_html = "<div style='border:4px solid Tomato;'><h3>Processing Error</h3><p>We found a valid start node, but the walking network within your inputs is too small. Please increase your target time or relocate and try again.</p></div>"

            return render(request, "routegen.html", 
            {
                'is_POST_request':True,
                'folium_map':m._repr_html_(), 
                'except_html':except_html,
                'target_time':target_time, 
                'number_of_nodes':number_of_nodes,
                'rand_lat':rand_lat,
                'rand_lon':rand_lon,                
            })
        except:
            print("EXCEPTED: unkown; MESSAGE: Try: call of buildmap_route() in routegen_view()")
                        
            # rebuild map
            m = buildmap_base(lat, lon)
            # exception html
            except_html = "<div style='border:4px solid Tomato;'><h3>Processing Error</h3><p>An unknown error occured. Please ask a Dev to consult the server logs and try again.</p></div>"

            return render(request, "routegen.html", 
            {
                'is_POST_request':True,
                'folium_map':m._repr_html_(), 
                'except_html':except_html,
                'target_time':target_time, 
                'number_of_nodes':number_of_nodes,
                'rand_lat':rand_lat,
                'rand_lon':rand_lon,                
            })

        # Save inputs to db
        print("Saving inputs to db:Mapgens...")
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
        print("Rendering new page...")

        # unit conversions.. metric to imperial
        route_distance = route_distance*0.00062137 # meters to miles
        route_time = route_distance / speed_miles_per_hour * 60 # minutes
        context = {
            'is_first_request':0,
            'target_time':target_time,
            'folium_map':m._repr_html_(),
            'routegen_exception':routegen_exception,
            'route_distance':round(route_distance, 1),
            'route_distance_metric':round(route_distance*1.609344, 1),
            'route_speed':round(speed_miles_per_hour, 1),
            'route_speed_metric':round(speed_miles_per_hour*1.609344, 1),
            'route_time':round(route_time, 1),
            'number_of_nodes':number_of_nodes,
            'rand_lat':rand_lat,
            'rand_lon':rand_lon,            
        }
        return render(request, "routegen.html", context)

def walk_view(request):
    # retrieve map inputs from session
    lat = request.session.get('lat')
    lon = request.session.get('lon')
    rand_lat = request.session.get('rand_lat')
    rand_lon = request.session.get('rand_lon')
    target_time = request.session.get('target_time')
    G = load_graphml(filepath=get_graph_filepath())
    route = request.session.get('route')

    # If the user landed here without storing necessary inputs first...
    # REDIRECT to '/routegen'
    if any([not rand_lat, not rand_lon, not target_time]):
        return redirect('/routegen')
    # REDIRECT to '/'
    elif any([not lat, not lon]):
        return redirect('')

    # Build the map
    # m = buildmap_base(lat, lon)
    # m = buildmap_route(m, target_time, (lat, lon), (rand_lat, rand_lon), G=G, route=route, plot_G=False)
    
    # create gdf of the route edges in order
    node_pairs = zip(route[:-1], route[1:])
    uvk = ((u, v, min(G[u][v], key=lambda k: G[u][v][k]["length"])) for u, v in node_pairs)
    gdf_edges = ox.utils_graph.graph_to_gdfs(G.subgraph(route), nodes=False).loc[uvk]
    print(gdf_edges)
    print(gdf_edges.columns)
    print(gdf_edges['geometry'].values[0])
    # create list [lat,lon] from gdf['geometry'].values linestrings.. N.B. poly.geometry api: https://isbe.bwk.tue.nl/education/Python/04_02_Shapely.html#linestring-specific-attributes
    linestrings = gdf_edges['geometry'].values
    route_polyline_arr = []
    for l in linestrings:
        for point in zip(*reversed(l.xy)): # l.xy = (np.array, np.array)
            route_polyline_arr.append(list(point)) # [lat, lon]
    print(route_polyline_arr)
    # # serialize list as json_dict
    # json_route_polyline_arr = ll_to_json(route_polyline_arr)
    # print(json_route_polyline_arr)
    # print(type(json_route_polyline_arr))

    # convert list of lists to json
    # json_route_polyline_arr = json.dumps(route_polyline_arr)
    # print(json_route_polyline_arr)
    # print(type(json_route_polyline_arr))
    # route_polyline_arr = [[lat, lon], [rand_lat, rand_lon]] # QUICK TEST

    return render(request, "walk.html", 
    {
        # 'folium_map':m._repr_html_(), 
        'lat':lat,
        'lon':lon,
        'rand_lat':rand_lat,
        'rand_lon':rand_lon,
        'route_polyline_arr':route_polyline_arr,
        # 'json_route_polyline_arr':json_route_polyline_arr, # list of [lat,lon] points
        'target_time':target_time,
    })