import folium

def buildmap_start(lat, lon):
    m = folium.Map(location=(lat, lon), zoom_start=17)
    folium.Marker(
        [lat, lon], 
        icon=folium.Icon(color='red', icon='home', prefix='fa'),
        tooltip='click here for detail', 
        popup='Start at ('+str(lat)+', '+str(lon)+')',
    ).add_to(m)
    return m._repr_html_()