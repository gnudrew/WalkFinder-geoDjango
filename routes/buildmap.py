import folium
import osmnx as ox
# import branca
# import re

def build_popup(title, lat, lon):
    popup_html = f"""
    <!-- import Bulma -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.2/css/bulma.min.css">
    <!-- content -->
    <div class="content is-small">
        <p>
            <strong>{title} at</strong><br>
            Lat: {lat}<br>
            Lon: {lon}
        </p>
    </div>
    """
    iframe = folium.IFrame(popup_html)
    return folium.Popup(iframe, min_width=110, max_width=200, height=150)

def buildmap_start(lat, lon):
    start_loc=(lat,lon)
    attribution = """
        Map data from &copy; <a href="https://openstreetmap.org/copyright">OpenStreetMap</a>,
        &copy; <a href="https://stadiamaps.com/">Stadia Maps</a>,   
        &copy; <a href="https://openmaptiles.org/">OpenMapTiles</a> 
    """
    m = folium.Map(
        location=start_loc, 
        zoom_start=16,
        # tiles="https://tiles.stadiamaps.com/tiles/outdoors/{z}/{x}/{y}{r}.png",
        attr=attribution,
        max_zoom=20,
    )

    folium.Marker(
        start_loc, 
        icon=folium.Icon(color='red', icon='home', prefix='fa'), 
        tooltip='click me', 
        popup=build_popup("Starting",lat,lon), 
    ).add_to(m)

    return m

def buildmap_route(m, target_time, start_loc, end_loc, G=None, route=None):
    # Given:
    # m : previous map
    # target_time : how long to walk in minutes
    # start_loc : starting location, tuple (lat,lon)
    # end_loc : ending location, tuple (lat,lon)
    # G : graph of walking network, MultiDiGraph object
    # route : route from starting location to ending location, list of nodes

    # set rezzom box for map after adding new marker
    # rezoom_box = [(start_loc[0]-.0025, start_loc[1]-.005), (start_loc[0]+.0025, start_loc[1]+.005)] # bounding box specified by two points: [southwest, northeast]

    # add marker at end_loc
    folium.Marker(
        end_loc,
        icon=folium.Icon(color='red', icon='reply', prefix='fa'),
        tooltip='click me',
        popup=build_popup("Turnaround",end_loc[0],end_loc[1]),
    ).add_to(m)

    # m.fit_bounds(rezoom_box)

    if G:
        # Plot graph, G, on the folium map
        m = ox.plot_graph_folium(G, graph_map=m)  
        if route:
            # plot the route on the folium map
            m = ox.plot_route_folium(G, route, route_map=m, color='#F72119')
            
    return m

def buildmap_walk(route, start_loc, end_loc):
# Given homebase map, start location, and end location, add route to end location.
# Assume homebase map has Marker object at start_loc, but no marker at end_loc.
    pass
# load route object

# generate end marker

# combine and return map, m.
