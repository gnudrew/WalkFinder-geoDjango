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

def build_marker_homebase(lat, lon):
    return folium.Marker(
        (lat, lon), 
        icon=folium.Icon(color='red', icon='home', prefix='fa'), 
        tooltip='click me', 
        popup=build_popup("Starting",lat,lon), 
    )

def build_marker_turnaround(lat, lon):
    return folium.Marker(
        (lat, lon),
        icon=folium.Icon(color='red', icon='reply', prefix='fa'),
        tooltip='click me',
        popup=build_popup("Turnaround",lat,lon),
    )

def buildmap_base(lat, lon):
    attribution = """
        Map data from &copy; <a href="https://openstreetmap.org/copyright">OpenStreetMap</a>,
        &copy; <a href="https://stadiamaps.com/">Stadia Maps</a>,   
        &copy; <a href="https://openmaptiles.org/">OpenMapTiles</a> 
    """
    m = folium.Map(
        location=(lat,lon), 
        zoom_start=16,
        # tiles="https://tiles.stadiamaps.com/tiles/outdoors/{z}/{x}/{y}{r}.png",
        attr=attribution,
        max_zoom=20,
    )

    build_marker_homebase(lat,lon).add_to(m)

    return m

def buildmap_route(m, target_time, start_loc, end_loc, G=None, route=None, plot_G=True):
    # Given:
    # m : previous map
    # target_time : how long to walk in minutes
    # start_loc : starting location, tuple (lat,lon)
    # end_loc : ending location, tuple (lat,lon)
    # G : graph of walking network, MultiDiGraph object
    # route : route from starting location to ending location, list of nodes

    # add marker at turnaround
    build_marker_turnaround(end_loc[0],end_loc[1]).add_to(m)

    if G:
        if plot_G == True:
            # Plot graph, G, on the folium map
            m = ox.plot_graph_folium(G, graph_map=m)
        if route:
            # plot the route on the folium map
            m = ox.plot_route_folium(G, route, route_map=m, color='#F72119')
        else:
            print("Error: Cannot plot Route without providing a graph, G.")
    return m