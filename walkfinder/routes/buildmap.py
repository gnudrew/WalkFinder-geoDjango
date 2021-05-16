import folium


def buildmap_start(lat, lon):
    start_loc=(lat,lon)
    m = folium.Map(location=start_loc, zoom_start=15)
    folium.Marker(
        start_loc, 
        icon=folium.Icon(color='red', icon='home', prefix='fa'),
        tooltip='click here for detail', 
        popup='Homebase at '+str(start_loc),
    ).add_to(m)

    return m

def buildmap_route(m, target_time, start_loc, end_loc):
    # add another feature to the map; placeholder for adding future route
    # randomly add a second marker within (lat+/.005, long+/-.01)


    # set rezzom box for map after adding new marker
    rezoom_box = [(start_loc[0]-.005, start_loc[1]-.01), (start_loc[0]+.005, start_loc[1]+.01)] # bounding box specified by two points: [southwest, northeast]

    print('======== buildmap_route() ========')
    print('start_loc is: ',start_loc)
    print('rand_loc is: ',end_loc)

    # add marker at rand_loc
    folium.Marker(
        end_loc, # hardcode something in for now
        icon=folium.Icon(color='blue'),
        tooltip='click here for detail',
        popup='Target time is '+str(target_time)+' min.',
    ).add_to(m)

    m.fit_bounds(rezoom_box)

    return m