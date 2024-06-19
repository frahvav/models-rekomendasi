from flask import Flask, request, jsonify
import joblib
import pandas as pd
from math import radians, cos, sin, sqrt, atan2

# Fungsi haversine untuk menghitung jarak
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # Radius bumi dalam kilometer
    
    dlat = radians(lat2 - lat1)
    dlon = radians(lon1 - lon2)
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

# Memuat dataset dan fungsi rekomendasi
df = joblib.load('places_dataset.pkl')
# Tidak perlu memuat recommend_places.pkl karena kita sudah mendefinisikan fungsi ini di atas

app = Flask(__name__)

@app.route('/')
def home():
    return "API untuk rekomendasi tempat!"

@app.route('/recommend', methods=['GET'])
def recommend():
    try:
        current_lat = float(request.args.get('lat'))
        current_lon = float(request.args.get('lon'))
        k = int(request.args.get('k', 5))
        
        recommendations = recommend_places(current_lat, current_lon, df, k)
        
        return jsonify(recommendations)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
 