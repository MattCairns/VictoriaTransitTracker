from google.transit import gtfs_realtime_pb2
from protobuf_to_dict import protobuf_to_dict
import folium, random
import requests
from helpers import *
feed = gtfs_realtime_pb2.FeedMessage()
response = requests.get('https://victoria.mapstrat.com/current/gtfrealtime_VehiclePositions.bin')
feed.ParseFromString(response.content)

buses = protobuf_to_dict(feed)

print('There are {} buses.'.format(len(feed.entity)))

bus = feed.entity[0]

trips = read_trips('data/trips.txt')
shapes = read_shapes('data/shapes.txt')

m = folium.Map(
    location=[48.427502, -123.367264],
    zoom_start=12,
    tiles='Stamen Terrain'
)

colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred',
             'lightred', 'darkblue', 'darkgreen', 'cadetblue',
             'darkpurple', 'lightblue', 'lightgreen',
             'gray', 'black']



for bus in feed.entity:
    trip_id = bus.vehicle.trip.trip_id
    if trip_id != '' and trip_id in trips:
        bus_name = trips[trip_id][3]

        if 'UVic Via Hillside' in bus_name:
            print(bus_name)
            c = random.choice(colors)
            folium.Marker([bus.vehicle.position.latitude, bus.vehicle.position.longitude],
                                popup=bus_name, icon=folium.Icon(color=c)).add_to(m)
            folium.PolyLine(shapes[trips[trip_id][7]], color=c).add_to(m)



m.save('index.html')
