from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np

app = Flask(__name__)

# with open("financial_planner_model.pkl", "rb") as f:
#     stock_ml_model = pickle.load(f)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/prediction")
def prediction():
    return render_template("prediction.html")

# @app.route("/api/predict_plan", methods=["POST"])
# def predict_plan():
#     data = request.get_json()
#     features = np.array([[
#         data["age"], data["income"], data["fixed_expenses"], data["variable_expenses"],
#         data["goal_amount"], data["goal_duration"], data["existing_savings"],
#         data["risk_code"], data["city_code"]
#     ]])
#     prediction = stock_ml_model.predict(features)[0]
#     return jsonify({
#         "recommended_saving": round(prediction[0], 2),
#         "recommended_investment": round(prediction[1], 2),
#         "recommended_essentials": round(prediction[2], 2),
#         "investment_distribution": {
#             "FD": f"{round(prediction[3]*100)}%",
#             "Gold": f"{round(prediction[4]*100)}%",
#             "Mutual Funds": f"{round(prediction[5]*100)}%",
#             "Stocks": f"{round(prediction[6]*100)}%"
#         }
#     })
from flask import Flask, request, jsonify
from flask_cors import CORS

CORS(app)  # This will enable CORS for all routes


import google.generativeai as genai

# 🔹 Configure API Key
genai.configure(api_key="AIzaSyAfsnTLNilyWNVTxFElpe0NAwI43EgU9EU")  # Replace with your Gemini API key

# 🔹 Initialize the Gemini Model
model = genai.GenerativeModel("gemini-2.0-flash")

# 🔹 Define the Function
input_string = ""
@app.route("/analyze", methods=["POST"])
def analyze_emails():
    all_bodies= request.get_json()
    print(all_bodies)
    return analyze_emails_with_gemini(all_bodies['email'])



def analyze_emails_with_gemini(all_bodies: str) -> str:
    """
    Accepts concatenated Gmail email bodies as a string and returns a summary of:
    [income, fixed, essential, lifestyle, savings]

    Returns '-1' for all if no info found; uses 0 for missing entries.
    """
    prompt = f"""
    You are an AI agent analyzing Gmail messages. Read the following email bodies and extract ONLY CASH TRANSACTION details.
    details is given at the last
    if any array index contain multiple value then take the sum of all the values in that index 
    mind it only one value will be there in each index and total index will be 5

    Group them into:
    1. Income
    2. Fixed Expenses
    3. Essential Expenses
    4. Lifestyle Expenses
    5. Savings

    only give the JSON array, no other text.
    Return a JSON array: [income, fixed, essential, lifestyle, savings]

    If none of the messages contain this info, return: [-1, -1, -1, -1, -1]
    If any value is not found, set it to 0.
    Example:
    [1000, 200, 300, 400, 500]
    Text is given:
    {all_bodies}
    """

    # 🔹 Send Prompt to Gemini
    try:
        response = model.generate_content([{"role": "user", "parts": [{"text": prompt}]}])
        result = response.text.strip()
        return midstage(result)  # Call midstage function to process the result
    except Exception as e:
        return f"Error generating content: {e}"
# print(analyze_emails_with_gemini("hello this is a test email with income 1000, fixed expenses 200, essential expenses 300, lifestyle expenses 400, savings 500"))


def give_output_of_analyze_emails_with_gemini(all_bodies: str) -> str:
    prompt = f"""
    You are a smart personal finance assistant. A user has received AI-predicted suggestions for reducing their expenses in the following categories. For each category, the percentage value may vary depending on the user's spending profile:
Text is given:

    {all_bodies}
    
    
    
Write a detailed, pointwise explanation for how the user can achieve the recommended percentage reduction in each category.
dont give ** in text just give html tags dont need page structure, just give the content in html format

For every category:

Briefly define what it includes.

Suggest practical ways to reduce expenses by approximately the given percentage.

Offer realistic, non-judgmental tips the user can follow immediately.

The output should be clear, crisp, and actionable — no emojis, no fluff.

Ensure that each bullet point feels personalized and helpful for someone trying to improve their monthly budgeting based on AI feedback.

Use the percentages dynamically and focus on making the advice realistic and easy to implement.

then give a break such that i can divide for the next part write a command %break% and then write the next part of the prompt

and make decision in this where to invest the savings to grow the money 

give points and how the money should be invested in the following categories:
    1. Fixed deposits
    2. Gold
    3. Mutual Funds
    4. Stocks
    5. others
 how much percentage should be invested in each category and why     

.    
    """

    # 🔹 Send Prompt to Gemini
    try:
        response = model.generate_content([{"role": "user", "parts": [{"text": prompt}]}])
        result = response.text.strip()

        return jsonify(result)
    except Exception as e:
        return f"Error generating content: {e}"





import numpy as np
import joblib
import json

def midstage(input_string: str) -> None:
# Load model
    ml_model = joblib.load("expense_reduction_model.pkl")

    # 🔹 Input string
    # input_string =  "```json[1475.13,2077.24,235.00,205.00,0]```"
    cleaned = input_string.replace("```json", "").replace("```", "").strip()
    print("Input String:", input_string)

    # 🔹 Convert JSON string to list
    original_array = json.loads(cleaned)  # -> [1000, 200, 300, 400, 500]

    # 🔹 Prepend default age (e.g., 30)
    age = 30
    sample_input = np.array([[age] + original_array])

    # 🔹 Make prediction
    prediction = ml_model.predict(sample_input)[0]

    # 🔹 Map predictions to categories
    categories = [
        "Fixed Expenses",
        "Variable Expenses",
        "Subscriptions",
        "Luxury Expenses"
    ]

    # 🔹 Print output
    output=" Suggested Expense Reductions Based on Your Profile:"

    for category, percent in zip(categories, prediction):
        #  output=output+"➤ {category}: Reduce by approximately {percent:.1f}%"
        output += f"\n➤ {category}: Reduce by approximately {percent:.1f}%"
   
   
    return give_output_of_analyze_emails_with_gemini(output)

# 🔹 Define the Function
    


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

