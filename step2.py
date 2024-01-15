import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from math import radians, cos, sin, asin, sqrt


file_path = 'data.xlsx'
incident_data = pd.read_excel(file_path)

# Priority Analysis
plt.figure(figsize=(12, 6))
sns.countplot(x='Priority', data=incident_data)
plt.title('Incident Priority Distribution')
plt.xlabel('Priority')
plt.ylabel('Number of Incidents')
plt.show()

# Deployment Time Analysis
plt.figure(figsize=(12, 6))
sns.boxplot(x='Priority', y='Deployment Time (hrs)', data=incident_data)
plt.title('Deployment Time by Incident Priority')
plt.xlabel('Priority')
plt.ylabel('Deployment Time (hrs)')
plt.show()

# Distance Calculation using Haversine Formula
def haversine(lon1, lat1, lon2, lat2):
    # Convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # Haversine formula
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371  # Radius of Earth in kilometers
    return c * r

# Coordinates of the three police stations
stations = {
    'Station1': {'Latitude': 55.868709, 'Longitude': -4.2579871},
    'Station2': {'Latitude': 55.849171, 'Longitude': -4.2164508},
    'Station3': {'Latitude': 55.830168, 'Longitude': -4.2468263}
}

# Calculate distances
for station, coords in stations.items():
    incident_data[station + '_Distance'] = incident_data.apply(lambda row: haversine(coords['Longitude'], coords['Latitude'], row['Longitude'], row['Latitude']), axis=1)

# Displaying the first few rows with the calculated distances
print(incident_data.head())
