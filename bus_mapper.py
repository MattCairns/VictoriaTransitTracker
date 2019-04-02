from google.transit import gtfs_realtime_pb2
import folium, random, requests
from folium import plugins
from helpers import *

gtfs = 'https://victoria.mapstrat.com/current/gtfrealtime_VehiclePositions.bin'

def get_realtime_data(link):
    feed = gtfs_realtime_pb2.FeedMessage()
    response = requests.get(link)
    feed.ParseFromString(response.content)
    return feed


def render_bus_locations(file_name):
    colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred',
                 'lightred', 'darkblue', 'darkgreen', 'cadetblue',
                 'darkpurple', 'lightblue', 'lightgreen',
                 'gray', 'black']


    feed = get_realtime_data(gtfs)

    print('There are {} buses.'.format(len(feed.entity)))

    trips = read_trips('data/trips.txt')
    shapes = read_shapes('data/shapes.txt')

    m = folium.Map(
        location=[48.427502, -123.367264],
        zoom_start=12,
        tiles='Stamen Terrain'
    )

    

    for bus in feed.entity:
        trip_id = bus.vehicle.trip.trip_id
        if trip_id != '' and trip_id in trips:
            bus_name = trips[trip_id][3]
            c = random.choice(colors)
            folium.Marker([bus.vehicle.position.latitude, bus.vehicle.position.longitude],
                          popup=bus_name, icon=folium.Icon(color=c)).add_to(m)
            folium.PolyLine(shapes[trips[trip_id][7]], color=c).add_to(m)


    m.save(file_name)


