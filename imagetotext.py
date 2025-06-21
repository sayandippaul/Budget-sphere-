# import google.generativeai as genai
# import base64
# import mimetypes

# # 🔹 Configure API Key
# genai.configure(api_key="AIzaSyDD8QW1BggDVVMLteDygHCHrD6Ff9Dy0e8")  # Replace with your actual API key

# # 🔹 Function to Convert Image to Proper Format
# def load_image_for_gemini(path):
#     mime_type, _ = mimetypes.guess_type(path)
#     with open(path, "rb") as f:
#         image_data = f.read()
#     return {
#         "inline_data": {
#             "mime_type": mime_type,
#             "data": base64.b64encode(image_data).decode("utf-8")
#         }
#     }

# # 🔹 Image Path
# image_path = "D:/Sikshasathi(ml)/handwritten.jpeg"

# # 🔹 Initialize the Gemini Vision Model
# model = genai.GenerativeModel("gemini-1.5-pro")

# # 🔹 Generate Response
# response = model.generate_content(
#     [
#         {"role": "user", "parts": [
#             {"text": "Extract all readable text from this image."},
#             load_image_for_gemini(image_path)
#         ]}
#     ]
# )

# # 🔹 Print the Extracted Text
# print("Extracted Text:\n", response.text)






# ekhan theke suru --------------------------------------------------------------------------------------------------------

import google.generativeai as genai

# 🔹 Configure API Key
genai.configure(api_key="AIzaSyAfsnTLNilyWNVTxFElpe0NAwI43EgU9EU")  # Replace with your Gemini API key

# 🔹 Initialize the Gemini Model
model = genai.GenerativeModel("gemini-2.0-flash")

# 🔹 Define the Function
def analyze_emails_with_gemini(all_bodies: str) -> str:
    """
    Accepts concatenated Gmail email bodies as a string and returns a summary of:
    [income, fixed, essential, lifestyle, savings]

    Returns '-1' for all if no info found; uses 0 for missing entries.
    """
    prompt = f"""
    You are an AI agent analyzing Gmail messages. Read the following email bodies and extract ONLY CASH TRANSACTION details.
    details is given at the last

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
        return result
    except Exception as e:
        return f"Error generating content: {e}"
# print(analyze_emails_with_gemini("hello this is a test email with income 1000, fixed expenses 200, essential expenses 300, lifestyle expenses 400, savings 500"))
input_string =analyze_emails_with_gemini("""
                                 Date 
Description 
January 1, 2018 – January 31, 2018 
Deposits 
LAND ACCESS TRAINING 
1/1/18 
Withdrawals 
Opening Balance   
Balance 
1/5/18 
$1,000.00 
Check #123 ABC Insurance  
1/7/18 
112.89 
ACH1 Withdrawal – Verizon Wireless  
887.11 
1/8/18 
85.00 
ATM Withdrawal – 350 Main St. 
Springfield, GA 
802.11 
200.00 
1/15/18 ACH Deposit – Acme Company Payroll 
1,475.13  
602.11 
1/16/18 Mortgage Loan Payment  
2,077.24 
1/17/18 Fee – Monthly Checking  
1,024.75 
1,052.49 
1/20/18 Check #124 – Bob’s Bakery  
5.00 
1,047.49 
1/29/18 ACH Withdrawal – Student Loan Servicing 
Co.  
35.00 
1,012.49 
163.50 
1/31/18 Ending Balance   
848.99 
848.99 
1ACH stands for Automated Clearing House – This term will generally appear on payments made online or direct 
deposits. 
LP1 Financial Document Samples 
Page 1 of 3 
 
 
 
 
Page 2 of 3 LP1 Financial Document Samples 
LAND ACCESS TRAINING FARMLAND FOR THE NEXT GENERATION 
Sample Ledger Book 
 
Date Description Credits Debits Running 
Profit 
Checkbook 
Balance 
1/1/18 Opening Balance    2,000.00 
3/1/18 Supplies - Seed Purchase  200.00 -200.00 1,800.00 
3/1/18 Supplies – Fertilizer  100.00 -300.00 1,700.00 
3/15/18 Labor – Prep and 
Planting 
 200.00 -500.00 1,500.00 
3/30/18 Labor – Growing  100.00 -600.00 1,400.00""")



def give_output_of_analyze_emails_with_gemini(all_bodies: str) -> str:
    prompt = f"""
    You are a smart personal finance assistant. A user has received AI-predicted suggestions for reducing their expenses in the following categories. For each category, the percentage value may vary depending on the user's spending profile:
Text is given:

    {all_bodies}
    
    
    
Write a detailed, pointwise explanation for how the user can achieve the recommended percentage reduction in each category.

For every category:

Briefly define what it includes.

Suggest practical ways to reduce expenses by approximately the given percentage.

Offer realistic, non-judgmental tips the user can follow immediately.

The output should be clear, crisp, and actionable — no emojis, no fluff.

Ensure that each bullet point feels personalized and helpful for someone trying to improve their monthly budgeting based on AI feedback.

Use the percentages dynamically and focus on making the advice realistic and easy to implement.
    
    """

    # 🔹 Send Prompt to Gemini
    try:
        response = model.generate_content([{"role": "user", "parts": [{"text": prompt}]}])
        result = response.text.strip()
        return result
    except Exception as e:
        return f"Error generating content: {e}"





import numpy as np
import joblib
import json

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

print(give_output_of_analyze_emails_with_gemini(output))

# 🔹 Define the Function
    
