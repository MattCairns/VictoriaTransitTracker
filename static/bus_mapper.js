BASECOORDS = [48.427502, -123.367264];

function makeMap() {
    var TILE_URL = "https://stamen-tiles-{s}.a.ssl.fastly.net/terrain/{z}/{x}/{y}.jpg";
    var MB_ATTR = 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';
    map = L.map('llmap').setView(BASECOORDS, 8);
    map.locate({setView: true, maxZoom: 18})
    map.on('locationfound', onLocationFound)
    L.tileLayer(TILE_URL, {attribution: MB_ATTR}).addTo(map);
}

var layer = L.layerGroup();

function renderBusses() {
    var arrowMarker = L.AwesomeMarkers.icon({
        icon: 'arrow-up',
        markerColor: 'red'
    });
    $.getJSON("/busses", function(obj) {

        // Add the busses
        var markers = obj.data.map(function(arr) {
            var bus = L.marker([arr[0], arr[1]]);
            bus.setIcon(arrowMarker);
            bus.bindPopup(arr[2])
            return bus;
        });

        // Add the bus route lines
        var lines = obj.data.map(function(arr) {
            var line = L.polyline(arr[3]);
            return line;
        });  

        // Remove top level layer and create new layer groups.
        map.removeLayer(layer);
        bus_layer = L.layerGroup(markers);
        lines_layer = L.layerGroup(lines);

        // Add the busses and lines to our map
        map.addLayer(bus_layer);
        map.addLayer(lines_layer);
    });
}


function onLocationFound(e) {
    var radius = e.accuracy / 2;

    L.marker(e.latlng).addTo(map)
        .bindPopup("You are within " + radius + " meters from this point");

    L.circle(e.latlng, radius).addTo(map);
}



$(function() {
    makeMap();
    renderBusses()

    // Refresh the bus locations every 30s
    var interval = setInterval(function() { renderBusses(); }, 30 * 1000);
})