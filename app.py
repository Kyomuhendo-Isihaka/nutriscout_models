from flask import Flask, request, jsonify
import pandas as pd
import json

app = Flask(__name__)

# Load the dataset
data = pd.read_excel("dataset.xlsx", header=None)
data.columns = ['AGE', 'BOYS_MEDIAN_HEIGHT', 'BOYS_SD_HEIGHT', 'GIRLS_MEDIAN_HEIGHT', 'GIRLS_SD_HEIGHT']
data = data.drop([0, 1])
data.reset_index(drop=True, inplace=True)

def calculate_z_score(value, median, standard_deviation):
    return (value - median) / standard_deviation

@app.route('/get_nutrition_recommendations', methods=['POST'])
def get_nutrition_recommendations():
    try:
        # Get input data from the POST request body
        input_data = request.get_json()
        
        # Extract values from the input data
        age = input_data.get('age')
        gender = input_data.get('gender').lower()
        height = input_data.get('height')
        weight = input_data.get('weight')
        # fname = input_data.get('fname'),
        # lname = input_data.get('lname'),
        # location = input_data.get('location'),
        
    except (ValueError, TypeError) as e:
        return jsonify({"Error": "Error reading inputs. Ensure the data is in the correct JSON format."}), 400

    # Validate input data
    if not isinstance(age, int) or age <= 0:
        return jsonify({"Error": "Invalid age. Please provide a positive integer value for age in months."}), 400
    if gender not in ['boy', 'girl']:
        return jsonify({"Error": "Invalid gender. Please specify 'boy' or 'girl'."}), 400
    if not (isinstance(height, (int, float)) and height > 0):
        return jsonify({"Error": "Invalid height. Please provide a positive number for height in cm."}), 400
    if not (isinstance(weight, (int, float)) and weight > 0):
        return jsonify({"Error": "Invalid weight. Please provide a positive number for weight in kg."}), 400
    
    # Filter data for the specific age
    standards = data[data['AGE'] == age]
    
    if standards.empty:
        return jsonify({"Error": f"No data available for age {age} months."}), 404
    
    # Extract gender-specific WHO data
    if gender == 'boy':
        median_height = standards['BOYS_MEDIAN_HEIGHT'].values[0]
        sd_height = standards['BOYS_SD_HEIGHT'].values[0]
    else:  # gender == 'girl'
        median_height = standards['GIRLS_MEDIAN_HEIGHT'].values[0]
        sd_height = standards['GIRLS_SD_HEIGHT'].values[0]
    
    # Calculate Z-scores for height
    height_z = calculate_z_score(height, median_height, sd_height)
    
    # Assess nutritional status for height (stunting)
    if height_z < -2:
        height_status = "Stunted Growth"
        height_recommendation = ("Increase protein intake, micronutrient supplements, ensure hygiene, "
                                 "and consult a healthcare professional for a tailored nutrition plan.")
    elif -2 <= height_z <= 2:
        height_status = "Normal Growth"
        height_recommendation = ("Maintain a balanced diet with a variety of nutrients. "
                                  "Incorporate more fruits, vegetables, and whole grains into daily meals.")
    else:
        height_status = "Above Average Growth"
        height_recommendation = ("Great growth! Keep up the healthy habits, and ensure you're staying active "
                                  "and getting enough rest. Continue with a balanced diet.")
    
    # Weight-based recommendation (BMI or weight-for-age)
    weight_status = "Normal Weight"
    weight_recommendation = "Maintain your healthy weight by balancing food intake with physical activity."
    
    # Additional recommendation for underweight or overweight children
    if weight < 5:  
        weight_status = "Underweight"
        weight_recommendation = ("Consider increasing calorie intake with nutrient-dense foods, such as avocados, "
                                  "nuts, and dairy products. Stay active and consult a healthcare professional.")
    elif weight > 10:  
        weight_status = "Overweight"
        weight_recommendation = ("Focus on a balanced diet with lower calorie intake, and engage in regular physical activity. "
                                  "Avoid sugary snacks and drinks, and consult a healthcare professional for guidance.")
    
    # Return the result as a JSON response
    return jsonify({
        
        "Height Z-score": round(height_z, 2),
        "Height Nutritional Status": height_status,
        "Height Recommendation": height_recommendation,
        "Weight Nutritional Status": weight_status,
        "Weight Recommendation": weight_recommendation
    })

if __name__ == '__main__':
    app.run(debug=True)
