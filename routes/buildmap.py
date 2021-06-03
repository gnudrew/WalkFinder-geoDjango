import folium
import osmnx as ox
import branca

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

    popup_html = f"""
        <h3 class="is-title is-small">Home at:</h3>
        <p class="">
        Lat: <span class="tag">{lat}</span><br>
        Lon: <span class="tag">{lon}</span>
        </p>
    """
    popup_iframe = branca.element.IFrame(html=popup_html,width=180,height=108)
    popup = folium.Popup(popup_iframe, max_width=180)
    folium.Marker(
        start_loc, 
        icon=folium.Icon(color='red', icon='home', prefix='fa'), 
        tooltip='clickable', 
        popup=popup, 
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

    # print('======== buildmap_route() ========')
    # print('start_loc is: ',start_loc)
    # print('rand_loc is: ',end_loc)

    # add marker at rand_loc
    folium.Marker(
        end_loc, # hardcode something in for now
        # colors:
        # purply-blue: #715EC1

        icon=folium.Icon(color='red', icon='reply', prefix='fa'),
        tooltip='clickable',
        popup='Turnback @',
    ).add_to(m)

    # m.fit_bounds(rezoom_box)

    if G:
        # Plot graph, G, on the folium map
        m = ox.plot_graph_folium(G, graph_map=m)  
        if route:
            # plot the route on the folium map
            m = ox.plot_route_folium(G, route, route_map=m, color='#F72119')
            
    return m

def buildmap_walk(m, start_loc, end_loc):
# Given homebase map, start location, and end location, add route to end location.
# Assume homebase map has Marker object at start_loc, but no marker at end_loc.
    pass
# generate route object


# generate end marker

# combine and return map, m.
