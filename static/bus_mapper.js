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

function renderData(districtid) {
    var arrowMarker = L.AwesomeMarkers.icon({
        icon: 'arrow-up',
        markerColor: 'red'
    });
    $.getJSON("/busses", function(obj) {
        var markers = obj.data.map(function(arr) {
            var bus = L.marker([arr[0], arr[1]]);
            bus.setIcon(arrowMarker);
            return bus;
        });
        map.removeLayer(layer);
        layer = L.layerGroup(markers);
        map.addLayer(layer);
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
    renderData('0');
    $('#distsel').change(function() {
        var val = $('#distsel option:selected').val();
        renderData(val);
    });
})