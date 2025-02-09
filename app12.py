# import os
# import numpy as np
# import tensorflow as tf
# from flask import Flask, request, jsonify
# from tensorflow.keras.preprocessing import image # type: ignore
# import base64
# import io
# from PIL import Image

# # Initialize Flask app
# app = Flask(__name__)

# # Load trained model
# model_path = 'palm_anemia_model.h5'
# if os.path.exists(model_path):
#     print("✅ Loading existing model...")
#     model = tf.keras.models.load_model(model_path)
# else:
#     raise FileNotFoundError(f"❌ Model file '{model_path}' not found! Train the model first.")

# # Function to preprocess image
# def preprocess_image(img):
#     img = img.resize((224, 224))  # Resize to match model input size
#     img_array = np.array(img) / 255.0  # Normalize pixel values
#     img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
#     return img_array

# # Flask API endpoint for prediction
# @app.route('/predict', methods=['POST'])
# def predict():
#     try:
#         data = request.get_json()
#         location = data.get('location', 'Unknown location')

#         if 'image' not in data:
#             return jsonify({"error": "Missing image data"}), 400

#         # Decode Base64 image
#         image_data = base64.b64decode(data['image'])
#         img = Image.open(io.BytesIO(image_data))

#         # Preprocess and predict
#         img_array = preprocess_image(img)
#         prediction = model.predict(img_array)

#         # Interpret result
#         if prediction < 0.5:
#             result = "Healthy"
#             recommendation = "Maintain a balanced diet and regular exercise."
#         else:
#             result = "Anemic"
#             recommendation = "Increase intake of iron-rich foods (spinach, lentils, red meat), vitamin B12 (eggs, dairy), and folate (leafy greens, beans)."

#         print(result)
#         return jsonify({"classification": result, "recommendation": recommendation})

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# # Run Flask app
# if __name__ == '__main__':
#     app.run(debug=True)


import os
import numpy as np
import tensorflow as tf
from flask import Flask, request, jsonify
from tensorflow.keras.preprocessing import image
import base64
import io
from PIL import Image

# Initialize Flask app
app = Flask(__name__)

# Load trained model
model_path = 'palm_anemia_model.h5'
if os.path.exists(model_path):
    print("✅ Loading existing model...")
    model = tf.keras.models.load_model(model_path)
else:
    raise FileNotFoundError(f"❌ Model file '{model_path}' not found! Train the model first.")

# Function to preprocess image
def preprocess_image(img):
    img = img.resize((224, 224))  # Resize to match model input size
    img_array = np.array(img) / 255.0  # Normalize pixel values
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    return img_array

# Recommendations based on region
def get_recommendation_for_region(region):
    recommendations = {
        "Central": (
            "Children in this region should consume more iron-rich foods such as fish, beans, leafy greens like dodo, and liver to boost their blood levels. "
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
        location = data.get('location', 'Unknown location')  # Default to 'Unknown location' if not provided

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
        else:
            region = "Northern"
    

        # Interpret result and recommendation
        if prediction < 0.5:  # Healthy
            result = "Healthy"
            recommendation = get_recommendation_for_region("Not Anemic")
        else:  # Anemic
            result = "Anemic"
            recommendation = get_recommendation_for_region(region)
        
        print(result)
        print(recommendation)

        return jsonify({
            "classification": result,
            "recommendation": recommendation,
            "location": location  # Send the location back in the response
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run Flask app
if __name__ == '__main__':
    app.run(debug=True)
