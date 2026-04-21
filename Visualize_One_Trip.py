import folium
import pandas as pd

# Load trip data 
df = pd.read_csv("trip_data.csv")
trip = df.iloc[0]  # first trip

# Create a map centered at start point
m = folium.Map(location=[trip['start_lat'], trip['start_lon']], zoom_start=14)
folium.Marker([trip['start_lat'], trip['start_lon']], popup='Start', icon=folium.Icon(color='green')).add_to(m)
folium.Marker([trip['end_lat'], trip['end_lon']], popup='End', icon=folium.Icon(color='red')).add_to(m)

# Add a line between start and end (straight line, not road‑based)
folium.PolyLine([(trip['start_lat'], trip['start_lon']), (trip['end_lat'], trip['end_lon'])], color='blue', weight=2.5, opacity=0.8).add_to(m)

# Save to HTML  
m.save('screenshots/geolife_trip_map.html')
print("Map saved as screenshots/geolife_trip_map.html – open and take a screenshot manually.")