from google.transit import gtfs_realtime_pb2
import random, requests
from helpers import *

gtfs = 'https://victoria.mapstrat.com/current/gtfrealtime_VehiclePositions.bin'
trips = read_static_data('data/trips.txt', index = 2)
routes = read_static_data('data/routes.txt')
shapes = read_shapes('data/shapes.txt')
trip_reference = read_static_data('data/trip_reference.txt')

def get_realtime_data(link):
    feed = gtfs_realtime_pb2.FeedMessage()
    response = requests.get(link)
    feed.ParseFromString(response.content)
    return feed


def get_data():
    # Get the realtime data deed
    feed = get_realtime_data(gtfs)

    # Bus locations and paths
    bus_locations = []
    bus_paths = []

    for bus in feed.entity:
        trip_id = bus.vehicle.trip.trip_id # Get the bus trip ID
        if trip_id in trip_reference:

            route_id = trip_reference[trip_id][3]   # Get the routes ID

            # Get other useful info
            bus_name = routes[route_id][3]
            route_short_name = routes[route_id][2]
            route_colour = '#' + routes[route_id][7]
            bus_popup = '<p style="text-align:center;"><b>' + route_short_name + '</b><br>' + bus_name + '</p>'

            # Add data to our lists
            bus_locations.append([bus.vehicle.position.latitude, bus.vehicle.position.longitude, bus_popup, route_colour])
            bus_paths.append([shapes[trips[trip_id][7]], route_colour])

    return bus_locations, bus_paths

def get_bus_locations():
    bus_locations, _ = get_data()
    return bus_locations

def get_bus_paths():
    _, bus_paths = get_data()
    return bus_paths

def main():
    get_data()
    print(trip_reference['1'])



if __name__ == '__main__':
    main()