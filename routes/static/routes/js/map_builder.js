// Assumes leaflet library has been loaded via CDN, e.g. in <head> tag.

function buildmap_base(lat, lon) {
    // Returns a leaflet map object with a home marker at the provided latitude and longitude.
    
    // init map
    var map = L.map('map').setView([lat, lon], 16)

    // add tiles
    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', 
        {
            attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
            maxZoom: 18,
            id: 'mapbox/streets-v11',
            tileSize: 512,
            zoomOffset: -1,
            accessToken: 'pk.eyJ1IjoiZ251ZHJldyIsImEiOiJjbDFhNTNpbmU1NzJhM29ycHR0cnpmd25sIn0.-rOcgOmj2C3ZimMeiHcBEQ'
        }).addTo(map);

    // add home marker
    var icon_home = L.icon({ // TASK --> build custom icons; figure out how folium does it, or do something whimsical with custom images
        // iconURL: 
    })
    var marker_home = L.marker([lat, lon], {
        // icon: icon_home,
    }).addTo(map)

    return map
}

function buildmap_route(
    lat_start,
    lon_start,
    lat_turnaround,
    lon_turnaround,
    route,
) {
    var map = buildmap_base(lat_start, lon_start)
    // add more stuff to the map
}

function buildmap_walk(
    lat_start,
    lon_start,
    lat_turnaround,
    lon_turnaround,
    route,
) {
    var map = buildmap_base(lat_start, lon_start)
    // add more stuff to the map
    
}