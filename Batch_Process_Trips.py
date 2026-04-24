import pandas as pd
import requests
import glob
import time
import traceback
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("ORS_API_KEY")

plt_files = glob.glob("C:/Users/HP/Downloads/Geolife Trajectories 1.3/Geolife Trajectories 1.3/Data/*/Trajectory/*.plt")
print(f"Found {len(plt_files)} .plt files")

# Limit to first 100 for testing
plt_files = plt_files[:100]

results = []

for file_path in plt_files:
    try:
        df = pd.read_csv(file_path, skiprows=6, header=None,
                         names=['lat', 'lon', 'altitude', 'field4', 'numeric_time', 'date', 'time'])
        df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'])
        
        if len(df) < 10:
            continue
        
        start_time = df['datetime'].iloc[0]
        end_time = df['datetime'].iloc[-1]
        actual_duration_min = (end_time - start_time).total_seconds() / 60
        
        start_lat, start_lon = df['lat'].iloc[0], df['lon'].iloc[0]
        end_lat, end_lon = df['lat'].iloc[-1], df['lon'].iloc[-1]
        
        # Euclidean distance approx in km
        dist_km = ((end_lat - start_lat)**2 + (end_lon - start_lon)**2)**0.5 * 111
        
        # ORS request
        url = f"https://api.openrouteservice.org/v2/directions/foot-walking?api_key={api_key}&start={start_lon},{start_lat}&end={end_lon},{end_lat}"
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            # Check if features exist and have summary
            if 'features' in data and len(data['features']) > 0:
                summary = data['features'][0].get('properties', {}).get('summary', {})
                ors_duration_min = summary.get('duration', None)
                if ors_duration_min:
                    ors_duration_min = ors_duration_min / 60
                else:
                    ors_duration_min = None
            else:
                ors_duration_min = None
        else:
            ors_duration_min = None
        
        results.append({
            'file': file_path,
            'start_lat': start_lat, 'start_lon': start_lon,
            'end_lat': end_lat, 'end_lon': end_lon,
            'dist_km': dist_km,
            'actual_duration_min': actual_duration_min,
            'ors_duration_min': ors_duration_min,
            'hour': start_time.hour,
            'day_of_week': start_time.dayofweek
        })
        
        time.sleep(0.2)
    except Exception as e:
        print(f"Error with {file_path}: {e}")
        # Continue to next file

# Save results
df_results = pd.DataFrame(results)
df_results.to_csv("trip_data.csv", index=False)
print(f"Saved {len(results)} trips to trip_data.csv")
print(df_results.head())