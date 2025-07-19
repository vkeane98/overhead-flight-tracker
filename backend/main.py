#!/usr/bin/env python3

from FlightRadar24 import FlightRadar24API
from fastapi import FastAPI
import json

FLIGHT_RADAR_DOMAIN = 'https://flightradar24.com/'
COOL_PLANES = ["777", "787", "A380", "747"]

def get_flights(fr_api):
    # bounds = fr_api.get_bounds_by_point(53.2410918, -6.1473695, 6000)
    bounds = fr_api.get_bounds_by_point(53.2410918, -6.1473695, 100000) # TODO make configurable
    flights = fr_api.get_flights(bounds = bounds)
    
    return filter_viewable_flights(fr_api, flights)

def filter_viewable_flights(fr_api, flights):
    viewable_flights = []
    for flight in flights:
        flight_details = fr_api.get_flight_details(flight)
        images = flight_details["aircraft"]["images"].get("large")[0]["link"]
        imageOrNoneStr = images if images else "NA"
        aircraft_type = flight_details["aircraft"]["model"]["text"]
        is_cool = any(cool_plane in flight_details["aircraft"]["model"]["text"] for cool_plane in COOL_PLANES)
        flight_altitude = int(flight.get_altitude().split(" ")[0])
        if flight_altitude < 15000 or is_cool:
            viewable_flights_dict = {
                "type": aircraft_type,
                "altitude": flight_altitude,
                "url": get_url(flight_details),
                "photo": imageOrNoneStr
            }
            viewable_flights.append(viewable_flights_dict)
    return viewable_flights
    

def get_url(flight_details):
    flight_radar_id = flight_details["identification"]["id"]
    callsign = flight_details["identification"]["callsign"]
    return FLIGHT_RADAR_DOMAIN + flight_radar_id + "/" + callsign

app = FastAPI()

@app.get("/overhead_flights")
def read_root():
    return get_flights(FlightRadar24API())

def main():
    fr_api = FlightRadar24API()
    flight_urls = get_flights(fr_api)

    print(flight_urls)

    # for flight_url in flight_urls:
    #     print(flight_url)

if __name__ == "__main__":
    main()




# /flights-overhead/details GET

# {
#     type: string
#     altitude: string
#     url: string
#     photo: string - path to source image
# }