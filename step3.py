import pandas as pd
import numpy as np

# Function to calculate Euclidean distance
def calculate_distance(lat1, lon1, lat2, lon2):
    return np.sqrt((lat2 - lat1)**2 + (lon2 - lon1)**2)

# Load the incident data from your actual file
incident_data = pd.read_excel('data.xlsx')

# Station coordinates (actual coordinates)
stations = {
    'Station1': {'Latitude': 55.868709, 'Longitude': -4.2579871},
    'Station2': {'Latitude': 55.870846, 'Longitude': -4.310066},  # New location for Station 2
    'Station3': {'Latitude': 55.830168, 'Longitude': -4.2468263}
}

# Add a column for each station distance
for station_id, coords in stations.items():
    incident_data[f'{station_id}_Distance'] = incident_data.apply(
        lambda row: calculate_distance(row['Latitude'], row['Longitude'], coords['Latitude'], coords['Longitude']), axis=1)

# Determine the nearest station for each incident
incident_data['Nearest Station'] = incident_data.apply(
    lambda row: min(stations.keys(), key=lambda x: row[f'{x}_Distance']), axis=1)

# Count incidents per station and shift
incidents_per_station_shift = incident_data.groupby(['Nearest Station', 'Hour']).size().unstack(fill_value=0)

# Output a summary of the data
incidents_per_station_shift
