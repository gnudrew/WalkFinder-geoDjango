from django.conf import settings
import os

from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from .models import Mapgens
from .buildmap import buildmap_base, buildmap_route

from django.contrib.gis.geos import Point
from random import random as r # interval r() -> x in [0,1)
import osmnx as ox
from networkx import NetworkXPointlessConcept
from osmnx.io import load_graphml, save_graphml


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
        print("Retrieving Stuf...")
        ## Retrieve form input
        target_time = int(request.POST.get('target_time'))
        # print("raw POST is_new:",request.POST.get('is_new_time'),"type:",type(request.POST.get('is_new_time')))
        is_new_time = int(request.POST.get('is_new_time')) #1=True,0=False
        # print("tt:",target_time,";convert bool is_new):",is_new_time)
        is_first_request = int(request.POST.get('is_first_request'))

        # store this to session
        request.session['target_time'] = target_time

        # retrieve map inputs from session
        lat = float(request.session['lat'])
        lon = float(request.session['lon'])
        
        ## Generate new graph if time changed, else load previous graph from memory
        # constants
        speed_meters_per_min = 80.45 # that's 3 mph walking speed
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
                G = ox.graph_from_point((lat,lon), network_type="walk", dist=distance/2, dist_type="network")
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

        ## Calculate a Random Route
        print("Calculating a random route...")
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
        # Store route to session
        request.session['route'] = route

        # build map from these inputs
        print("Building a new Map...")
        m = buildmap_base(lat, lon)
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

        context = {
            'is_first_request':0,
            'target_time':target_time, 
            'folium_map':m._repr_html_(), 
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
    m = buildmap_base(lat, lon)
    m = buildmap_route(m, target_time, (lat, lon), (rand_lat, rand_lon), G=G, route=route, plot_G=False)
    
    return render(request, "walk.html", 
    {
        'folium_map':m._repr_html_(), 
        'lat':lat,
        'lon':lon,
        'rand_lat':rand_lat,
        'rand_lon':rand_lon,
        'target_time':target_time,
    })
