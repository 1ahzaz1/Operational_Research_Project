import pandas as pd
from collections import defaultdict



# Reading the entire incident and station data from the Excel file
# We'll use the pandas library for this task

# Read the incidents and stations data from the Excel file
all_incidents = pd.read_excel('data.xlsx', sheet_name=0)
all_stations = pd.read_excel('data.xlsx', sheet_name=1)

# Displaying the first few rows of each to confirm successful loading
# print(all_incidents.head())
# print(all_stations.head())
# all_incidents_shape = all_incidents.shape
# all_stations_shape = all_stations.shape

# print(all_incidents_shape) 
# print(all_stations_shape)



# Constants for shift times and number of officers
SHIFT_TIMES = {
    'Early': (0, 7),   # 0-7 hours
    'Day': (8, 15),    # 8-15 hours
    'Night': (16, 23)  # 16-23 hours
}
OFFICERS_PER_SHIFT = {
    'Early': 15,
    'Day': 25,
    'Night': 40
}


def get_shift(hour):
    """Determine the shift based on the hour."""
    for shift, (start, end) in SHIFT_TIMES.items():
        if start <= hour <= end:
            return shift
    return None


def simulate_responses_flat_distance(incidents, stations):
    """Simulate responses to incidents with a simplified flat distance calculation."""
    # Constants for distance calculation
    LATITUDE_MILE_CONVERSION = 69  # Approx. miles per degree of latitude
    LONGITUDE_MILE_CONVERSION = 54.6  # Approx. miles per degree of longitude (varies by latitude, this is an approximation for Glasgow)

    def flat_distance(lat1, lon1, lat2, lon2):
        """Calculate the approximate flat distance in miles between two points."""
        delta_lat = (lat1 - lat2) * LATITUDE_MILE_CONVERSION
        delta_lon = (lon1 - lon2) * LONGITUDE_MILE_CONVERSION
        return ((delta_lat ** 2) + (delta_lon ** 2)) ** 0.5

    # Dictionary to track the availability of officers in each station during each shift
    officers_available = {shift: {station: OFFICERS_PER_SHIFT[shift] for station in stations['Station No.']} 
                          for shift in SHIFT_TIMES}

    # List to store response details
    responses = []

    # Sort incidents by priority and hour
    incidents_sorted = incidents.sort_values(by=['Priority', 'Hour'])

    # Simulate responses
    for _, incident in incidents_sorted.iterrows():
        nearest_station, distance = find_nearest_station(incident, stations, flat_distance)
        shift = get_shift(incident['Hour'])
        
        # Check if there are available officers in the nearest station
        if officers_available[shift][nearest_station] > 0:
            officers_available[shift][nearest_station] -= 1  # Assign an officer
            response = {
                'URN': incident['URN'],
                'Station No.': nearest_station,
                'Shift': shift,
                'Hour': incident['Hour'],
                'Priority': incident['Priority'],
                'Distance': distance  # Flat distance to the incident
            }
            responses.append(response)

    return pd.DataFrame(responses)

# Function to find nearest station with flat distance calculation
def find_nearest_station(incident, stations, distance_function):
    """Find the nearest station to an incident using a provided distance function."""
    min_distance = float('inf')
    nearest_station = None
    for _, station in stations.iterrows():
        distance = distance_function(incident['Latitude'], incident['Longitude'], 
                                     station['Latitude'], station['Longitude'])
        if distance < min_distance:
            min_distance = distance
            nearest_station = station['Station No.']
    return nearest_station, min_distance

# Re-run the simulation with flat distance calculation
responses_simulation_flat_distance = simulate_responses_flat_distance(all_incidents, all_stations)
print(responses_simulation_flat_distance.head())  # Display the first few rows of the simulation results

responses_simulation_flat_distance.to_csv('results')



























# def simulate_responses(incidents, stations):
#     """Simulate responses to incidents."""
#     # Dictionary to track the availability of officers in each station during each shift
#     officers_available = {shift: {station: OFFICERS_PER_SHIFT[shift] for station in stations['Station No.']} 
#                           for shift in SHIFT_TIMES}

#     # List to store response details
#     responses = []

#     # Sort incidents by priority and hour
#     incidents_sorted = incidents.sort_values(by=['Priority', 'Hour'])

#     # Simulate responses
#     for _, incident in incidents_sorted.iterrows():
#         nearest_station, _ = find_nearest_station(incident, stations)
#         shift = get_shift(incident['Hour'])
        
#         # Check if there are available officers in the nearest station
#         if officers_available[shift][nearest_station] > 0:
#             officers_available[shift][nearest_station] -= 1  # Assign an officer
#             response = {
#                 'URN': incident['URN'],
#                 'Station No.': nearest_station,
#                 'Shift': shift,
#                 'Hour': incident['Hour'],
#                 'Priority': incident['Priority']
#             }
#             responses.append(response)

#     return pd.DataFrame(responses)

# # Simulate the responses to all incidents
# responses_simulation = simulate_responses(all_incidents, all_stations)
# print(responses_simulation.head())  # Display the first few rows of the simulation results











# Function for calculating travel times from each station to each incident
# def calculate_all_travel_times(incidents, stations):
#     """
#     Calculate travel times from each station to each incident.

#     :param incidents: DataFrame containing incidents data.
#     :param stations: DataFrame containing stations data.
#     :return: DataFrame containing travel times for each incident-station pair.
#     """
#     # Create an empty DataFrame to store travel times
#     travel_times = pd.DataFrame(columns=['URN', 'Station No.', 'Travel Time'])

#     # Iterate over each incident-station pair and calculate travel time
#     for incident_index, incident in incidents.iterrows():
#         for station_index, station in stations.iterrows():
#             travel_time = calculate_travel_time(incident['Latitude'], incident['Longitude'], 
#                                                 station['Latitude'], station['Longitude'])
#             travel_times = travel_times.append({
#                 'URN': incident['URN'],
#                 'Station No.': station['Station No.'],
#                 'Travel Time': travel_time
#             }, ignore_index=True)

#     return travel_times

# # Calculate travel times for the loaded data
# all_travel_times = calculate_all_travel_times(all_incidents, all_stations)
# all_travel_times.head()
