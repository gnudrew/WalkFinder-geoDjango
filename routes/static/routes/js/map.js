// Create the map; set starting center and zoom
var mymap = L.map('mapid').setView([51.505, -0.09], 13);
// Add a marker to the map
var marker = L.marker([51.5, -0.09]).addTo(mymap);
// Add a circle
var circle = L.circle([51.508, -0.11], {
    color: 'red',
    fillColor: '#f03',
    fillOpacity: 0.5,
    radius: 500
}).addTo(mymap);
// Add a polygon
var polygon = L.polygon([
    [51.509, -0.08],
    [51.503, -0.06],
    [51.51, -0.047]
]).addTo(mymap);
