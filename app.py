from flask import Flask, request, jsonify
import pandas as pd
import os
import numpy as np
import tensorflow as tf
from flask import Flask, request, jsonify
from tensorflow.keras.preprocessing import image # type: ignore
import base64
import io
from PIL import Image

app = Flask(__name__)

# Load the dataset
data = pd.read_excel("dataset.xlsx", header=None)
data.columns = ['AGE', 'BOYS_MEDIAN_HEIGHT', 'BOYS_SD_HEIGHT', 'GIRLS_MEDIAN_HEIGHT', 'GIRLS_SD_HEIGHT']
data = data.drop([0, 1])
data.reset_index(drop=True, inplace=True)

# Region-based recommendations
region_recommendations = {
    "Central": {
        "Stunting": "Provide a balanced diet rich in proteins (eggs, fish, beans), energy-giving foods (sweet potatoes, matoke), and vegetables for vitamins.",
        "Wasting": "Ensure high-energy foods like full-fat milk, millet porridge, and groundnut paste. Seek medical help for severe cases.",
        "Underweight": "Increase meal frequency and include foods like avocado, peanut sauce, and fresh fruits. If no improvement, consult a nutritionist."
    },
    "Western": {
        "Stunting": "Include milk, millet bread, beef, and leafy greens. Regular checkups are recommended to monitor growth.",
        "Wasting": "Give high-energy foods such as millet porridge, ghee, roasted groundnuts, and milk. Seek medical care for severe cases.",
        "Underweight": "Increase portions of protein-rich foods (beans, chicken) and serve meals with avocado. Encourage fresh milk consumption."
    },
    "Eastern": {
        "Stunting": "Encourage millet porridge with groundnut paste, rice with fish, and leafy greens. Seek medical assessment if stunting persists.",
        "Wasting": "Provide fish, energy-rich porridge with milk, and fresh fruit. Severe cases require immediate medical attention.",
        "Underweight": "Increase portions of rice, beans, and cassava, and add roasted groundnuts. Fresh fruits and vegetables improve overall health."
    },
    "Northern": {
        "Stunting": "Give nutrient-rich foods like sorghum bread, goat meat, and leafy greens. Periodic health checkups are essential.",
        "Wasting": "Include sorghum porridge with groundnut paste, dry fish, and sim-sim. Seek urgent medical attention for severe malnutrition.",
        "Underweight": "Increase meals with protein (goat meat, beans) and energy foods (cassava, avocado). If weight gain is slow, seek medical advice."
    }
}

def calculate_z_score(value, median, sd):
    return (value - median) / sd

@app.route('/get_nutrition_recommendations', methods=['POST'])
def get_nutrition_recommendations():
    try:
        input_data = request.get_json()
        age = input_data.get('age')
        gender = input_data.get('gender').lower()
        height = input_data.get('height')
        weight = input_data.get('weight')
        location = input_data.get('location')

        if not isinstance(age, int) or age <= 0:
            return jsonify({"Error": "Invalid age. Provide a positive integer (in months)."}), 400
        if gender not in ['boy', 'girl']:
            return jsonify({"Error": "Invalid gender. Specify 'boy' or 'girl'."}), 400
        if not (isinstance(height, (int, float)) and height > 0):
            return jsonify({"Error": "Invalid height. Provide a positive number in cm."}), 400
        if not (isinstance(weight, (int, float)) and weight > 0):
            return jsonify({"Error": "Invalid weight. Provide a positive number in kg."}), 400
        if location not in region_recommendations:
            return jsonify({"Error": "Invalid location. Choose from 'Central', 'Western', 'Eastern', or 'Northern'."}), 400

        # Get WHO standards for the given age
        standards = data[data['AGE'] == age]
        if standards.empty:
            return jsonify({"Error": f"No data available for age {age} months."}), 404

        # Extract median and SD for height
        if gender == 'boy':
            median_height = standards['BOYS_MEDIAN_HEIGHT'].values[0]
            sd_height = standards['BOYS_SD_HEIGHT'].values[0]
        else:
            median_height = standards['GIRLS_MEDIAN_HEIGHT'].values[0]
            sd_height = standards['GIRLS_SD_HEIGHT'].values[0]

        # Calculate Z-score for height
        height_z = calculate_z_score(height, median_height, sd_height)

        # Determine height status and region-based recommendation
        if height_z < -2:
            height_status = "Stunted Growth"
            height_recommendation = region_recommendations[location]["Stunting"]
        elif -2 <= height_z <= 2:
            height_status = "Normal Growth"
            height_recommendation = "Maintain a balanced diet with a variety of nutrients."
        else:
            height_status = "Above Average Growth"
            height_recommendation = "Ensure a healthy diet and active lifestyle."

        # Determine weight status and region-based recommendation
        if weight < 5:
            weight_status = "Underweight"
            weight_recommendation = region_recommendations[location]["Underweight"]
        elif weight > 10:
            weight_status = "Overweight"
            weight_recommendation = "Focus on a balanced diet with controlled calorie intake."
        else:
            weight_status = "Normal Weight"
            weight_recommendation = "Maintain a healthy diet and lifestyle."

        # Determine wasting status and region-based recommendation
        if height_z < -3:
            wasting_status = "Severe Wasting"
            wasting_recommendation = region_recommendations[location]["Wasting"]
        else:
            wasting_status = "Normal"
            wasting_recommendation = "Maintain a good balance of protein, carbohydrates, and fats."

        return jsonify({
            "Height Z-score": round(height_z, 2),
            "Height Nutritional Status": height_status,
            "Height Recommendation": height_recommendation,
            "Weight Nutritional Status": weight_status,
            "Weight Recommendation": weight_recommendation,
            "Wasting Status": wasting_status,
            "Wasting Recommendation": wasting_recommendation,
            "Region": location
        })

    except Exception as e:
        return jsonify({"Error": str(e)}), 500



# Load trained model
model_path = 'palm_anemia_model.h5'
if os.path.exists(model_path):
    print("✅ Loading existing model...")
    model = tf.keras.models.load_model(model_path)
else:
    raise FileNotFoundError(f"❌ Model file '{model_path}' not found! Train the model first.")

# Function to preprocess image
def preprocess_image(img):
    img = img.resize((224, 224))  
    img_array = np.array(img) / 255.0  
    img_array = np.expand_dims(img_array, axis=0) 
    return img_array


# Recommendations based on region
def get_recommendation_for_region(region):
    recommendations = {
        "Central": (
            "Child should consume more iron-rich foods such as fish, beans, leafy greens like dodo, and liver to boost their blood levels. "
            "Iron absorption is improved by taking these foods with vitamin C sources such as oranges, mangoes, and passion fruits. "
            "If a child frequently looks pale or weak, seek medical advice to check for anemia and possible supplementation."
        ),
        "Western": (
            "To prevent and manage anemia, children should eat milk, eggs, beef liver, beans, and dark leafy greens like spinach. "
            "Consuming iron-rich meals with fresh fruits like guavas and pineapples enhances iron absorption. "
            "Regular deworming and malaria prevention are also important in this region, as parasites can cause anemia. "
            "If signs of severe tiredness or dizziness persist, visit a healthcare facility for blood tests and treatment."
        ),
        "Eastern": (
            "Including groundnuts, beans, and millet porridge in a child’s diet helps combat anemia. Fresh vegetables such as dodo and pumpkin leaves provide additional iron and folic acid. "
            "If a child remains weak and unresponsive to diet changes, consult a health worker for further evaluation."
        ),
        "Northern": (
            "A diet rich in sorghum, goat meat, dry fish, and iron-rich vegetables like cowpea leaves can help fight anemia. "
            "Drinking fresh fruit juices (such as orange or tamarind juice) alongside meals improves iron absorption. "
            "Since infections like malaria and worm infestations contribute to anemia, regular deworming and malaria prevention are essential. "
            "If a child remains fatigued, seek medical attention immediately."
        ),
        "Not Anemic": (
            "Although your child is not anemic, maintaining a balanced diet with iron-rich foods like beans, fish, and leafy greens, alongside vitamin C sources such as oranges and mangoes, will help prevent future deficiencies."
        ),
    }
    
    return recommendations.get(region, "Region not recognized. Please provide a valid region.")

# Flask API endpoint for prediction
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        # Retrieve location (if available)
        location = data.get('location', 'Unknown location')  
        print(location)

        if 'image' not in data:
            return jsonify({"error": "Missing image data"}), 400

        # Decode Base64 image
        image_data = base64.b64decode(data['image'])
        img = Image.open(io.BytesIO(image_data))

        # Preprocess and predict
        img_array = preprocess_image(img)
        prediction = model.predict(img_array)

        # Determine the region (mocking for this example)
        if 'Central' in location:
            region = "Central"
        elif 'Western' in location:
            region = "Western"
        elif 'Eastern' in location:
            region = "Eastern"
        elif 'Northern' in location:
            region = "Nortern"
        else:
            region = "Not Anemic"
    

        # Interpret result and recommendation
        if prediction < 0.5:  # Healthy
            result = "No Anemia Detected"
            recommendation = get_recommendation_for_region("Not Anemic")
        else:  # Anemic
            result = "Anemia Detected"
            recommendation = get_recommendation_for_region(region)
        
        print(result)
        print(recommendation)

        return jsonify({
            "classification": result,
            "recommendation": recommendation,
            "location": location  
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500




if __name__ == '__main__':
    app.run(debug=True)
