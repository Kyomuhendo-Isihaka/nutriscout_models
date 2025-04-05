# from flask import Flask, request, jsonify
# import pandas as pd
# import os
# import numpy as np
# import tensorflow as tf
# from flask import Flask, request, jsonify
# from tensorflow.keras.preprocessing import image # type: ignore
# import base64
# import io
# from PIL import Image

# app = Flask(__name__)

# # Load the dataset
# data = pd.read_excel("dataset.xlsx", header=None)
# data.columns = ['AGE', 'BOYS_MEDIAN_HEIGHT', 'BOYS_SD_HEIGHT', 'GIRLS_MEDIAN_HEIGHT', 'GIRLS_SD_HEIGHT']
# data = data.drop([0, 1])
# data.reset_index(drop=True, inplace=True)

# # Region-based recommendations
# region_recommendations = {
#     "Central": {
#         "Stunting": "Provide a balanced diet rich in proteins (eggs, fish, beans), energy-giving foods (sweet potatoes, matoke), and vegetables for vitamins.",
#         "Wasting": "Ensure high-energy foods like full-fat milk, millet porridge, and groundnut paste. Seek medical help for severe cases.",
#         "Underweight": "Increase meal frequency and include foods like avocado, peanut sauce, and fresh fruits. If no improvement, consult a nutritionist."
#     },
#     "Western": {
#         "Stunting": "Include milk, millet bread, beef, and leafy greens. Regular checkups are recommended to monitor growth.",
#         "Wasting": "Give high-energy foods such as millet porridge, ghee, roasted groundnuts, and milk. Seek medical care for severe cases.",
#         "Underweight": "Increase portions of protein-rich foods (beans, chicken) and serve meals with avocado. Encourage fresh milk consumption."
#     },
#     "Eastern": {
#         "Stunting": "Encourage millet porridge with groundnut paste, rice with fish, and leafy greens. Seek medical assessment if stunting persists.",
#         "Wasting": "Provide fish, energy-rich porridge with milk, and fresh fruit. Severe cases require immediate medical attention.",
#         "Underweight": "Increase portions of rice, beans, and cassava, and add roasted groundnuts. Fresh fruits and vegetables improve overall health."
#     },
#     "Northern": {
#         "Stunting": "Give nutrient-rich foods like sorghum bread, goat meat, and leafy greens. Periodic health checkups are essential.",
#         "Wasting": "Include sorghum porridge with groundnut paste, dry fish, and sim-sim. Seek urgent medical attention for severe malnutrition.",
#         "Underweight": "Increase meals with protein (goat meat, beans) and energy foods (cassava, avocado). If weight gain is slow, seek medical advice."
#     }
# }

# # # Region-based food recommendations and a 7-day meal plan
# # region_recommendations = {
# #     "Central": {
# #         "Stunting": {
# #             "recommendation": "Provide a balanced diet rich in proteins (eggs, fish, beans), energy-giving foods (sweet potatoes, matoke), and vegetables for vitamins.",
# #             "weeklyPlan": {
# #                 "Day 1": "Millet porridge with milk and groundnuts, boiled eggs, and a piece of fruit.",
# #                 "Day 2": "Mashed sweet potatoes with avocado, fish stew with vegetables.",
# #                 "Day 3": "Beans and rice, steamed vegetables, boiled matoke (plantain).",
# #                 "Day 4": "Eggs with spinach, whole wheat bread, fruit salad.",
# #                 "Day 5": "Groundnut paste with millet porridge and carrots.",
# #                 "Day 6": "Vegetable soup with beans, maize, and avocados.",
# #                 "Day 7": "Fish stew with cassava, leafy greens, and fruits."
# #             }
# #         },
# #         "Wasting": {
# #             "recommendation": "Ensure high-energy foods like full-fat milk, millet porridge, and groundnut paste. Seek medical help for severe cases.",
# #             "weeklyPlan": {
# #                 "Day 1": "Full-fat milk with millet porridge, groundnut paste, and fruit.",
# #                 "Day 2": "Roasted groundnuts with banana, boiled sweet potatoes with butter.",
# #                 "Day 3": "High-energy porridge with added milk, boiled eggs, and avocado.",
# #                 "Day 4": "Full-fat milk with ghee, fried groundnuts, and mashed beans.",
# #                 "Day 5": "Groundnut paste with millet porridge, scrambled eggs, and fruit.",
# #                 "Day 6": "Sweet potatoes with avocado, full-fat milk, and roasted chicken.",
# #                 "Day 7": "Millet porridge with milk, groundnut paste, and fresh fruit."
# #             }
# #         },
# #         "Underweight": {
# #             "recommendation": "Increase meal frequency and include foods like avocado, peanut sauce, and fresh fruits. If no improvement, consult a nutritionist.",
# #             "weeklyPlan": {
# #                 "Day 1": "Peanut butter sandwich, full-fat milk, and a fruit.",
# #                 "Day 2": "Sweet potatoes with groundnut sauce, fruit salad.",
# #                 "Day 3": "Boiled beans with avocado, a glass of milk.",
# #                 "Day 4": "Roast chicken with mashed potatoes and avocado.",
# #                 "Day 5": "Avocado toast with a boiled egg, full-fat milk.",
# #                 "Day 6": "Groundnut paste with millet porridge, bananas.",
# #                 "Day 7": "Rice with beans and avocado, fruit juice."
# #             }
# #         }
# #     },
# #     "Western": {
# #         "Stunting": {
# #             "recommendation": "Include milk, millet bread, beef, and leafy greens. Regular checkups are recommended to monitor growth.",
# #             "weeklyPlan": {
# #                 "Day 1": "Millet bread with groundnut paste, boiled eggs, and fruit.",
# #                 "Day 2": "Beef stew with rice, leafy greens, and a glass of milk.",
# #                 "Day 3": "Fish with cassava, avocado, and steamed vegetables.",
# #                 "Day 4": "Beans and maize, avocado, and banana.",
# #                 "Day 5": "Beef stew with millet bread, spinach.",
# #                 "Day 6": "Eggs with tomatoes, bread, and orange juice.",
# #                 "Day 7": "Rice with peas, milk, and carrots."
# #             }
# #         },
# #         "Wasting": {
# #             "recommendation": "Give high-energy foods such as millet porridge, ghee, roasted groundnuts, and milk. Seek medical care for severe cases.",
# #             "weeklyPlan": {
# #                 "Day 1": "Millet porridge with ghee, full-fat milk, and roasted groundnuts.",
# #                 "Day 2": "Sweet potatoes with avocado, groundnut paste, and bananas.",
# #                 "Day 3": "Full-fat milk with millet porridge, scrambled eggs.",
# #                 "Day 4": "Porridge with groundnuts, roasted chicken, and fruit.",
# #                 "Day 5": "Ghee with porridge, boiled eggs, and mango.",
# #                 "Day 6": "Roasted groundnuts with banana, full-fat milk, and millet bread.",
# #                 "Day 7": "Groundnut paste with porridge, avocado, and fruit."
# #             }
# #         },
# #         "Underweight": {
# #             "recommendation": "Increase portions of protein-rich foods (beans, chicken) and serve meals with avocado. Encourage fresh milk consumption.",
# #             "weeklyPlan": {
# #                 "Day 1": "Chicken with rice, avocado, and full-fat milk.",
# #                 "Day 2": "Beans and avocado, boiled egg, fresh fruit.",
# #                 "Day 3": "Beef stew with potatoes, avocado, and milk.",
# #                 "Day 4": "Eggs with beans, millet porridge with milk.",
# #                 "Day 5": "Chicken stew with rice and vegetables, banana.",
# #                 "Day 6": "Groundnut paste with sweet potatoes, avocado.",
# #                 "Day 7": "Rice with beans, avocado, and fruit juice."
# #             }
# #         }
# #     },
# #     "Eastern": {
# #         "Stunting": {
# #             "recommendation": "Encourage millet porridge with groundnut paste, rice with fish, and leafy greens. Seek medical assessment if stunting persists.",
# #             "weeklyPlan": {
# #                 "Day 1": "Millet porridge with groundnut paste, steamed vegetables, and fish.",
# #                 "Day 2": "Rice with fish and vegetables, boiled eggs.",
# #                 "Day 3": "Beans with avocado, fruit salad.",
# #                 "Day 4": "Boiled sweet potatoes, groundnut paste, and leafy greens.",
# #                 "Day 5": "Fish stew with cassava and vegetables.",
# #                 "Day 6": "Rice with beans, boiled eggs, and fruit.",
# #                 "Day 7": "Groundnut paste with millet porridge, boiled chicken."
# #             }
# #         },
# #         "Wasting": {
# #             "recommendation": "Provide fish, energy-rich porridge with milk, and fresh fruit. Severe cases require immediate medical attention.",
# #             "weeklyPlan": {
# #                 "Day 1": "Fish with energy-rich porridge, full-fat milk, and fruit.",
# #                 "Day 2": "Millet porridge with groundnut paste, bananas.",
# #                 "Day 3": "Sweet potatoes with avocado, milk, and fruits.",
# #                 "Day 4": "Groundnut paste with porridge, fresh fruit, and eggs.",
# #                 "Day 5": "Millet porridge with groundnuts, boiled chicken.",
# #                 "Day 6": "High-energy porridge with milk, roasted groundnuts, and fruit.",
# #                 "Day 7": "Fish stew with cassava, vegetables, and milk."
# #             }
# #         },
# #         "Underweight": {
# #             "recommendation": "Increase portions of rice, beans, and cassava, and add roasted groundnuts. Fresh fruits and vegetables improve overall health.",
# #             "weeklyPlan": {
# #                 "Day 1": "Rice with beans and avocado, fruit.",
# #                 "Day 2": "Cassava with groundnut paste, fruit juice.",
# #                 "Day 3": "Steamed beans with sweet potatoes and avocado.",
# #                 "Day 4": "Rice with beans and avocado, full-fat milk.",
# #                 "Day 5": "Fried groundnuts with cassava, banana.",
# #                 "Day 6": "Beans with rice, vegetables, and fruit.",
# #                 "Day 7": "Groundnut paste with porridge, avocado, and fruit."
# #             }
# #         }
# #     },
# #     "Northern": {
# #         "Stunting": {
# #             "recommendation": "Give nutrient-rich foods like sorghum bread, goat meat, and leafy greens. Periodic health checkups are essential.",
# #             "weeklyPlan": {
# #                 "Day 1": "Sorghum bread with groundnut paste, goat meat stew.",
# #                 "Day 2": "Rice with goat meat and vegetables.",
# #                 "Day 3": "Beans with cassava, avocado, and fruit.",
# #                 "Day 4": "Steamed beans with sorghum bread, avocado.",
# #                 "Day 5": "Goat meat stew with vegetables, rice.",
# #                 "Day 6": "Sorghum porridge with groundnuts, avocado.",
# #                 "Day 7": "Goat meat with vegetables, sorghum bread."
# #             }
# #         },
# #         "Wasting": {
# #             "recommendation": "Include sorghum porridge with groundnut paste, dry fish, and sim-sim. Seek urgent medical attention for severe malnutrition.",
# #             "weeklyPlan": {
# #                 "Day 1": "Sorghum porridge with groundnut paste, dry fish.",
# #                 "Day 2": "Sorghum porridge with sim-sim, boiled eggs.",
# #                 "Day 3": "Groundnut paste with cassava, bananas.",
# #                 "Day 4": "Sim-sim with rice, fruit.",
# #                 "Day 5": "Sorghum bread with groundnuts, boiled eggs.",
# #                 "Day 6": "Groundnut paste with millet, fish.",
# #                 "Day 7": "Sorghum porridge with milk, fruit."
# #             }
# #         },
# #         "Underweight": {
# #             "recommendation": "Increase meals with protein (goat meat, beans) and energy foods (cassava, avocado). If weight gain is slow, seek medical advice.",
# #             "weeklyPlan": {
# #                 "Day 1": "Goat meat stew with rice, avocado.",
# #                 "Day 2": "Beans with cassava, avocado, and fruit.",
# #                 "Day 3": "Roasted chicken with millet porridge and vegetables.",
# #                 "Day 4": "Goat meat with sweet potatoes, full-fat milk.",
# #                 "Day 5": "Rice with beans, avocado, and fresh fruit.",
# #                 "Day 6": "Groundnut paste with millet porridge, chicken.",
# #                 "Day 7": "Cassava with groundnut paste, fresh fruit."
# #             }
# #         }
# #     }
# # }



# def calculate_z_score(value, median, sd):
#     return (value - median) / sd

# #change# Function to calculate BMI (Body Mass Index)
# def calculate_bmi(weight, height):
#     # BMI = weight(kg) / height(m)^2
#     height_m = height / 100  # Convert height from cm to meters
#     bmi = weight / (height_m ** 2)
#     return bmi

# @app.route('/get_nutrition_recommendations', methods=['POST'])
# def get_nutrition_recommendations():
#     try:
#         input_data = request.get_json()
#         age = input_data.get('age')
#         gender = input_data.get('gender').lower()
#         height = input_data.get('height')
#         weight = input_data.get('weight')
#         location = input_data.get('location')

#         if not isinstance(age, int) or age <= 0:
#             return jsonify({"Error": "Invalid age. Provide a positive integer (in months)."}), 400
#         if gender not in ['boy', 'girl']:
#             return jsonify({"Error": "Invalid gender. Specify 'boy' or 'girl'."}), 400
#         if not (isinstance(height, (int, float)) and height > 0):
#             return jsonify({"Error": "Invalid height. Provide a positive number in cm."}), 400
#         if not (isinstance(weight, (int, float)) and weight > 0):
#             return jsonify({"Error": "Invalid weight. Provide a positive number in kg."}), 400
#         if location not in region_recommendations:
#             return jsonify({"Error": "Invalid location. Choose from 'Central', 'Western', 'Eastern', or 'Northern'."}), 400

#         # Get WHO standards for the given age
#         standards = data[data['AGE'] == age]
#         if standards.empty:
#             return jsonify({"Error": f"No data available for age {age} months."}), 404

#         # Extract median and SD for height
#         if gender == 'boy':
#             median_height = standards['BOYS_MEDIAN_HEIGHT'].values[0]
#             sd_height = standards['BOYS_SD_HEIGHT'].values[0]
#         else:
#             median_height = standards['GIRLS_MEDIAN_HEIGHT'].values[0]
#             sd_height = standards['GIRLS_SD_HEIGHT'].values[0]

#         # Calculate Z-score for height
#         height_z = calculate_z_score(height, median_height, sd_height)
#         bmi = calculate_bmi(weight, height)

        

#         # Determine height status and region-based recommendation
#         if height_z < -2:
#             height_status = "Stunted Growth"
#             height_recommendation = region_recommendations[location]["Stunting"]
#         elif -3 <= height_z <= 2:
#             height_status = "Normal Growth"
#             height_recommendation = "Maintain a balanced diet with a variety of nutrients."
#         else:
#             height_status = "Above Average Growth"
#             height_recommendation = "Ensure a healthy diet and active lifestyle."

        
#          # Change #Calculate BMI to determine underweight or overweight
         
        
#          #chnage# Determine weight status (underweight, normal weight, or overweight) based on BMI
#         if bmi < -3:
#             weight_status = "Underweight"
#             weight_recommendation = region_recommendations[location]["Underweight"]
#         elif 1 <= bmi < 2:
#             weight_status = "Overweight"
#             weight_recommendation = "Focus on a balanced diet with controlled calorie intake."
#         else:
#             weight_status = "Normal Weight"
        
        
        
#         # Determine weight status and region-based recommendation
#         # if weight < 5:
#         #     weight_status = "Underweight"
#         #     weight_recommendation = region_recommendations[location]["Underweight"]
#         # elif weight > 10:
#         #     weight_status = "Overweight"
#         #     weight_recommendation = "Focus on a balanced diet with controlled calorie intake."
#         # else:
#         #     weight_status = "Normal Weight"
#         #     weight_recommendation = "Maintain a healthy diet and lifestyle."


#         # Determine wasting status and region-based recommendation
#         if height_z < -3:
#             wasting_status = "Severe Wasting"
#             wasting_recommendation = region_recommendations[location]["Wasting"]
#         else:
#             wasting_status = "Normal"
#             wasting_recommendation = "Maintain a good balance of protein, carbohydrates, and fats."

#         return jsonify({
#             "Height Z-score": round(height_z, 2),
#             "Height Nutritional Status": height_status,
#             "Height Recommendation": height_recommendation,
#             "Weight Nutritional Status": weight_status,
#             "Weight Recommendation": weight_recommendation,
#             "BMI": round(bmi, 2),
#             "Wasting Status": wasting_status,
#             "Wasting Recommendation": wasting_recommendation,
#             "Region": location
#         })

#     except Exception as e:
#         return jsonify({"Error": str(e)}), 500




# if __name__ == '__main__':
#     app.run(debug=True)



from flask import Flask, request, jsonify
import pandas as pd
import numpy as np

app = Flask(__name__)

# Load datasets with exact row positions from your Excel file
# Height-for-age (rows 3-63)
height_data = pd.read_excel("dataset.xlsx", header=None, skiprows=3, nrows=61)
height_data.columns = ['AGE', 'BOYS_MEDIAN_HEIGHT', 'BOYS_SD_HEIGHT', 'GIRLS_MEDIAN_HEIGHT', 'GIRLS_SD_HEIGHT']

# Weight-for-age (rows 67-127)
weight_data = pd.read_excel("dataset.xlsx", header=None, skiprows=67, nrows=61)
weight_data.columns = ['AGE', 'BOYS_MEDIAN_WEIGHT', 'BOYS_SD_WEIGHT', 'GIRLS_MEDIAN_WEIGHT', 'GIRLS_SD_WEIGHT']

# Weight-for-height (rows 131-231)
wfh_data = pd.read_excel("dataset.xlsx", header=None, skiprows=131, nrows=101)
wfh_girls = wfh_data.iloc[:, :3].copy()  # Columns A-C
wfh_girls.columns = ['HEIGHT', 'GIRLS_MEDIAN_WEIGHT', 'GIRLS_SD_WEIGHT']
wfh_boys = wfh_data.iloc[:, 3:].copy()   # Columns D-E
wfh_boys.columns = ['HEIGHT', 'BOYS_MEDIAN_WEIGHT', 'BOYS_SD_WEIGHT']

# Region recommendations (maintaining your exact format)
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

def get_closest_height_data(height, gender):
    """Get weight-for-height data for the closest height"""
    data = wfh_girls if gender == 'girl' else wfh_boys
    idx = (data['HEIGHT'] - height).abs().idxmin()
    return data.loc[idx]

@app.route('/get_nutrition_recommendations', methods=['POST'])
def get_nutrition_recommendations():
    try:
        input_data = request.get_json()
        age = int(input_data.get('age'))
        gender = input_data.get('gender').lower()
        height = float(input_data.get('height'))
        weight = float(input_data.get('weight'))
        location = input_data.get('location')

        # Validate inputs
        if not (1 <= age <= 60):
            return jsonify({"Error": "Age must be between 1-60 months."}), 400
        if gender not in ['boy', 'girl']:
            return jsonify({"Error": "Gender must be 'boy' or 'girl'."}), 400
        if height <= 0 or weight <= 0:
            return jsonify({"Error": "Height and weight must be positive values."}), 400
        if location not in region_recommendations:
            return jsonify({"Error": "Invalid location specified."}), 400

        # 1. Height-for-age calculation
        hfa_row = height_data[height_data['AGE'] == age]
        if hfa_row.empty:
            return jsonify({"Error": f"No height data for age {age} months."}), 404
            
        median_height = hfa_row[f"{gender.upper()}S_MEDIAN_HEIGHT"].values[0]
        sd_height = hfa_row[f"{gender.upper()}S_SD_HEIGHT"].values[0]
        height_z = calculate_z_score(height, median_height, sd_height)

        # 2. Weight-for-age calculation
        wfa_row = weight_data[weight_data['AGE'] == age]
        if wfa_row.empty:
            return jsonify({"Error": f"No weight data for age {age} months."}), 404
            
        median_weight = wfa_row[f"{gender.upper()}S_MEDIAN_WEIGHT"].values[0]
        sd_weight = wfa_row[f"{gender.upper()}S_SD_WEIGHT"].values[0]
        weight_z = calculate_z_score(weight, median_weight, sd_weight)

        # 3. Weight-for-height (wasting) calculation
        wfh_row = get_closest_height_data(height, gender)
        wfh_z = calculate_z_score(weight, wfh_row[f"{gender.upper()}S_MEDIAN_WEIGHT"], 
                                 wfh_row[f"{gender.upper()}S_SD_WEIGHT"])

        # Classifications (maintaining your exact wording)
        height_status = "Stunted Growth" if height_z < -2 else "Normal Growth" if -2 <= height_z <= 2 else "Above Average Growth"
        weight_status = "Underweight" if weight_z < -2 else "Normal Weight" if -2 <= weight_z <= 1 else "Overweight"
        wasting_status = "Severe Wasting" if wfh_z < -3 else "Moderate Wasting" if -3 <= wfh_z < -2 else "Normal"

        # Recommendations (using your exact format)
        height_rec = region_recommendations[location]["Stunting"] if height_z < -2 else "Maintain a balanced diet with a variety of nutrients."
        weight_rec = region_recommendations[location]["Underweight"] if weight_z < -2 else "Maintain a healthy diet and lifestyle."
        wasting_rec = region_recommendations[location]["Wasting"] if wfh_z < -2 else "Maintain a good balance of protein, carbohydrates, and fats."

        return jsonify({
            "Height Z-score": round(height_z, 2),
            "Height Nutritional Status": height_status,
            "Height Recommendation": height_rec,
            "Weight-for-Age Z-score": round(weight_z, 2),
            "Weight Nutritional Status": weight_status,
            "Weight Recommendation": weight_rec,
            "Weight-for-Height Z-score": round(wfh_z, 2),
            "Wasting Status": wasting_status,
            "Wasting Recommendation": wasting_rec,
            "Region": location
        })

    except Exception as e:
        return jsonify({"Error": f"Server error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
