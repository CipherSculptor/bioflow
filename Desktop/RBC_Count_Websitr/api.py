import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LinearRegression
import joblib
import os

app = Flask(__name__)
# Configure CORS to allow requests from any origin with any headers
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*", "allow_headers": "*", "expose_headers": "*"}})

# Global variables to store our trained models and preprocessing objects
encoder = None
scaler = None
model_rbc = None
model_wbc = None
model_platelets = None
model_hemoglobin = None
valid_blood_groups = ['A+', 'B+', 'O+']

def load_or_train_models():
    global encoder, scaler, model_rbc, model_wbc, model_platelets, model_hemoglobin
    
    # Check if models are already saved
    if os.path.exists('models/model_rbc.joblib'):
        # Load pre-trained models
        encoder = joblib.load('models/encoder.joblib')
        scaler = joblib.load('models/scaler.joblib')
        model_rbc = joblib.load('models/model_rbc.joblib')
        model_wbc = joblib.load('models/model_wbc.joblib')
        model_platelets = joblib.load('models/model_platelets.joblib')
        model_hemoglobin = joblib.load('models/model_hemoglobin.joblib')
    else:
        # Load and prepare data
        try:
            data = pd.read_csv('CBC_REPORT_PERMITTIVITY.csv', thousands=',')
        except FileNotFoundError:
            # Sample data if file not found (for development purposes)
            print("Warning: CSV file not found. Using sample data.")
            data = pd.DataFrame({
                'Blood Group': ['A+', 'B+', 'O+'] * 10,
                'Permittivity': np.random.normal(70, 10, 30),
                'RBC Count': np.random.normal(5, 0.5, 30),
                'WBC Count': np.random.normal(8000, 1000, 30),
                'Platelets': np.random.normal(250000, 50000, 30),
                'Hemoglobin': np.random.normal(14, 1.5, 30)
            })
        
        # Filter data
        data = data[data['Blood Group'].isin(valid_blood_groups)]
        
        # Preprocess data
        encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
        blood_group_encoded = encoder.fit_transform(data[['Blood Group']])
        
        scaler = StandardScaler()
        numerical_features = scaler.fit_transform(data[['Permittivity']])
        
        X = np.hstack((numerical_features, blood_group_encoded))
        y_rbc = data['RBC Count']
        y_wbc = data['WBC Count']
        y_platelets = data['Platelets']
        y_hemoglobin = data['Hemoglobin']
        
        # Train models
        model_rbc = LinearRegression()
        model_wbc = LinearRegression()
        model_platelets = LinearRegression()
        model_hemoglobin = LinearRegression()
        
        model_rbc.fit(X, y_rbc)
        model_wbc.fit(X, y_wbc)
        model_platelets.fit(X, y_platelets)
        model_hemoglobin.fit(X, y_hemoglobin)
        
        # Save models
        os.makedirs('models', exist_ok=True)
        joblib.dump(encoder, 'models/encoder.joblib')
        joblib.dump(scaler, 'models/scaler.joblib')
        joblib.dump(model_rbc, 'models/model_rbc.joblib')
        joblib.dump(model_wbc, 'models/model_wbc.joblib')
        joblib.dump(model_platelets, 'models/model_platelets.joblib')
        joblib.dump(model_hemoglobin, 'models/model_hemoglobin.joblib')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        print("Received data:", data)  # Debug logging
        
        # Extract data from request
        permittivity = float(data['permittivity'])
        blood_group = data['bloodGroup']
        name = data['name']
        
        print(f"Extracted - Name: {name}, Blood Group: {blood_group}, Permittivity: {permittivity}")  # Debug logging
        
        # Validate blood group
        if blood_group not in valid_blood_groups:
            print(f"Invalid blood group: '{blood_group}', Valid groups are: {valid_blood_groups}")  # Debug logging
            return jsonify({
                'error': f'Invalid blood group. Accepted values are {", ".join(valid_blood_groups)}'
            }), 400
        
        # Preprocess input
        new_data_point_scaled = scaler.transform([[permittivity]])
        new_data_point_encoded = encoder.transform([[blood_group]])
        new_data = np.hstack((new_data_point_scaled, new_data_point_encoded))
        
        # Make predictions
        predicted_rbc = model_rbc.predict(new_data)[0]
        predicted_wbc = model_wbc.predict(new_data)[0]
        predicted_platelets = model_platelets.predict(new_data)[0]
        predicted_hemoglobin = model_hemoglobin.predict(new_data)[0]
        
        # Format and return predictions
        return jsonify({
            'name': name,
            'blood_group': blood_group,
            'rbc_count': f"{predicted_rbc:.2f} millions/cumm",
            'wbc_count': f"{predicted_wbc:.2f} /microliter",
            'platelets_count': f"{int(predicted_platelets)} /microliter",
            'hemoglobin': f"{predicted_hemoglobin:.2f} g/dL"
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/test', methods=['GET'])
def test():
    return jsonify({
        'status': 'success',
        'message': 'API is working!'
    })

if __name__ == '__main__':
    load_or_train_models()
    app.run(debug=True, host='0.0.0.0', port=5070) 