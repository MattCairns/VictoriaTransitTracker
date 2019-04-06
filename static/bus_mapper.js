BASECOORDS = [48.427502, -123.367264];

function makeMap() {
    var TILE_URL = "https://stamen-tiles-{s}.a.ssl.fastly.net/terrain/{z}/{x}/{y}.jpg";
    var MB_ATTR = 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> | <a href="https://www.bctransit.com/">BCTransit</a>';
    map = L.map('llmap').setView(BASECOORDS, 8);
    map.locate({setView: true, maxZoom: 18})
    map.on('locationfound', onLocationFound)
    L.tileLayer(TILE_URL, {attribution: MB_ATTR}).addTo(map);
}

function renderBusses() {
    $.getJSON("/busses", function(obj) {
        // Add the busses
        var busses = obj.data.map(function(arr) {
            var latitude = arr[0];
            var longitude = arr[1];
            var message = arr[2];
            var colour = arr[3];
            var bus = L.marker([latitude, longitude]);
            bus.setIcon(
                L.AwesomeMarkers.icon({
                    icon: 'arrow-up',
                    markerColor: 'cadetblue',
                    iconColor: colour
                })
            );
            bus.bindPopup(message)
            return bus;
        });
        
        // Remove top level layer and create new layer groups.
        bus_layer = L.layerGroup(busses);

        // Add the busses and lines to our map
        map.addLayer(bus_layer);
    });

}


function renderPaths() {
    $.getJSON("/paths", function(obj) {
        console.log(obj);
        // Add the bus route lines
        var lines = obj.data.map(function(arr) {
            var line = L.polyline(arr[0]);
            line.setStyle({ color: arr[1] });
            return line;
        });  
        lines_layer = L.layerGroup(lines);
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
    var interval = setInterval(function() { 
        map.removeLayer(bus_layer);

        renderBusses(); 
    }, 30 * 1000);
    renderPaths();
})