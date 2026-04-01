# using the sydneytrains.json file to plot the train routes on a map
import json
# can we use custom theme maps 
import folium
# load the json file
with open("sydneytrains.json", "r") as f:
    data = json.load(f)
# create a map centered on sydney
sydney_map = folium.Map(location=[-33.8688, 151.2093], zoom_start=10)
# loop through the train routes and add them to the map
for route in data["i"]:
    coordinates = route["geometry"]["coordinates"]
    # convert the coordinates to lat, lon format
    lat_lon = [(coord[1], coord[0]) for coord in coordinates]
    # add the route to the map
    folium.PolyLine(lat_lon, color="blue", weight=2.5, opacity=1).add_to(sydney_map)
# save the map to an html file
sydney_map.save("sydney_trains_map.html")
print("Map saved to sydney_trains_map.html")