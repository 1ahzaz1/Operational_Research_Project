import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import MarkerCluster

# Load the data
file_path = 'data.xlsx'  # Replace with your file path
incident_data = pd.read_excel(file_path)

# Visualize incident frequency by Day and Hour
sns.set(style="whitegrid")

# Plotting incident frequency by Day
plt.figure(figsize=(12, 6))
sns.countplot(x='Day', data=incident_data)
plt.title('Incident Frequency by Day of the Week')
plt.xlabel('Day of the Week')
plt.ylabel('Number of Incidents')
plt.show()

# Plotting incident frequency by Hour
plt.figure(figsize=(12, 6))
sns.countplot(x='Hour', data=incident_data)
plt.title('Incident Frequency by Hour of the Day')
plt.xlabel('Hour of the Day')
plt.ylabel('Number of Incidents')
plt.show()

# Geographic Distribution of Incidents
# Sample the data to avoid overloading the map (adjust sample size as needed)
sampled_data = incident_data.sample(n=2272, random_state=1)

# Create a map centered around the average latitude and longitude
map_center = [sampled_data['Latitude'].mean(), sampled_data['Longitude'].mean()]
incident_map = folium.Map(location=map_center, zoom_start=12)

# Add a marker cluster to the map
marker_cluster = MarkerCluster().add_to(incident_map)

# Coordinates of the three police stations
stations = {
    'Station1': {'Latitude': 55.868709, 'Longitude': -4.2579871},
    'Station2': {'Latitude': 55.849171, 'Longitude': -4.2164508},
    'Station3': {'Latitude': 55.830168, 'Longitude': -4.2468263}
}

# Adding markers for the police stations
for station, coords in stations.items():
    folium.Marker(location=[coords['Latitude'], coords['Longitude']],
                  popup=station,
                  icon=folium.Icon(color='red', icon='star')).add_to(incident_map)

# Add each incident as a marker to the cluster
for idx, row in sampled_data.iterrows():
    folium.Marker(location=[row['Latitude'], row['Longitude']],
                  popup=f"URN: {row['URN']}<br>Priority: {row['Priority']}<br>Deployment Time: {row['Deployment Time (hrs)']} hrs").add_to(marker_cluster)

# Save and display the map
incident_map.save('incident_map.html')
