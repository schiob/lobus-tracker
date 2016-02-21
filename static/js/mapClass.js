var map = L.map('map')
map.setView([25.426933, -100.970340], 13);

var markerLayerGroup = L.layerGroup().addTo(map);

L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 18,
    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a> Written by <a href="http://www.bitmasons.com">Gordon Haff</a>. Running on OpenShift by Red Hat. <a href="http://bitmason.blogspot.com/p/blog-page_18.html"> About.</a>'
}).addTo(map);

function getPins(e){
    bounds = map.getBounds();
    url = "/data";
    $.get(url, pinTheMap, "json");
}

function pinTheMap(data)
{
    map.removeLayer(markerLayerGroup);
    if (map.getZoom() > 8) {
        var markerArray = new Array(data["trucks"].length)
        for (var i = 0; i < data["trucks"].length; i++) {
            truck = data["trucks"][i];
            markertext = "<b>"+truck.id + "</b><br \>Dir " + truck.dir + "</b><br \>Hora " + truck.timestamp
            markerArray[i] = L.marker([truck.pos[0], truck.pos[1]],{title: truck.id, riseOnHover: true}).bindPopup(markertext);
        }
        markerLayerGroup = L.layerGroup(markerArray).addTo(map);
    }
}

function foundme(e)
{
    if (e.latlng.lat > 24 && e.latlng.lat < 50 && e.latlng.lng < -66 && e.latlng.lng > -124) {
        map.panTo(e.latlng);
    }
}

map.on('dragend', getPins);
map.on('zoomend', getPins);
map.whenReady(getPins);
