from django.conf import settings
import os

from django.shortcuts import render, redirect

from routes.route_generator import RouteGenerator
from .models import Mapgens
from .buildmap import buildmap_base, buildmap_route

from django.contrib.gis.geos import Point
from random import random as r # interval r() -> x in [0,1)
import osmnx as ox
from networkx import NetworkXPointlessConcept
from osmnx.io import load_graphml, save_graphml

class GraphWrangler:

    def get_graph_filepath():
        base_dir = settings.BASE_DIR
        save_dir = os.path.join(base_dir, "data")
        filepath = os.path.join(save_dir, "G.graphml") # use 1 file for PoC
        return filepath

    def create_graph(self, lat, lon, dist):
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

    def load_graph(self,):
        pass