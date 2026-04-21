import pandas as pd
import requests
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("ORS_API_KEY")

file_path = r"C:\Users\HP\Downloads\Geolife Trajectories 1.3\Geolife Trajectories 1.3\Data\000\Trajectory\20090629173335.plt" 

# Skip first 6 header lines, then read 7 columns
df = pd.read_csv(file_path, skiprows=6, header=None,
                 names=['lat', 'lon', 'altitude', 'field4', 'numeric_time', 'date', 'time'])

# Combine date and time
df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'])

# Calculate speed between consecutive points (km/h)
df['lat_next'] = df['lat'].shift(-1)
df['lon_next'] = df['lon'].shift(-1)
df['time_next'] = df['datetime'].shift(-1)

# Approximate distance using haversine (simplified: 111 km per degree)
df['dist_km'] = ((df['lat_next'] - df['lat'])**2 + (df['lon_next'] - df['lon'])**2)**0.5 * 111
df['time_diff_hours'] = (df['time_next'] - df['datetime']).dt.total_seconds() / 3600
df['speed_kmh'] = df['dist_km'] / df['time_diff_hours']

# Keep points where speed > 1 km/h (moving)
moving = df[df['speed_kmh'] > 1]

if len(moving) > 1:
    moving_time_min = (moving['datetime'].iloc[-1] - moving['datetime'].iloc[0]).total_seconds() / 60
    print(f"Moving time (excluding stops): {moving_time_min:.2f} min")

# Actual travel time
start_time = df['datetime'].iloc[0]
end_time = df['datetime'].iloc[-1]
actual_duration_min = (end_time - start_time).total_seconds() / 60

# Get start and end coordinates (these should now be correct)
start_lat, start_lon = df['lat'].iloc[0], df['lon'].iloc[0]
end_lat, end_lon = df['lat'].iloc[-1], df['lon'].iloc[-1]

print(f"Start: ({start_lat}, {start_lon})")
print(f"End: ({end_lat}, {end_lon})")
print(f"Actual duration: {actual_duration_min:.2f} min")

load_dotenv()
api_key = os.getenv("ORS_API_KEY")
url = f"https://api.openrouteservice.org/v2/directions/driving-car?api_key={api_key}&start={start_lon},{start_lat}&end={end_lon},{end_lat}"

response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    ors_duration_min = data['features'][0]['properties']['summary']['duration'] / 60
    print(f"ORS estimated duration: {ors_duration_min:.2f} min")
    print(f"Difference (Actual - ORS): {actual_duration_min - ors_duration_min:.2f} min")
else:
    print(f"ORS error: {response.status_code}")