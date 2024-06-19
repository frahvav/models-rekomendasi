import pandas as pd
import joblib
from math import radians, cos, sin, sqrt, atan2

# Fungsi haversine untuk menghitung jarak
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # Radius bumi dalam kilometer
    
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    distance = R * c
    return distance

# Fungsi rekomendasi
def recommend_places(current_lat, current_lon, df, k=5):
    distances = []
    
    for index, row in df.iterrows():
        distance = haversine(current_lat, current_lon, row['Latitude'], row['Longitude'])
        distances.append((row['Place_name'], row['Address1'], distance))
    
    distances = sorted(distances, key=lambda x: x[2])
    recommended_places = distances[:k]
    
    return recommended_places

# Memuat dataset
df = pd.read_csv('dataset.csv')
df = df.dropna(subset=['Latitude', 'Longitude'])

# Menyimpan dataset dan fungsi
joblib.dump(df, 'places_dataset.pkl')
joblib.dump(recommend_places, 'recommend_places.pkl')
