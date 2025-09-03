# from flask import Flask, request, render_template
#
# app = Flask(__name__)
#
# @app.route('/')
# def home():
#     return  "hello" #render_template('Python.html')
#
# @app.route('/run_script', methods=['POST'])
# def run_script():
#     # Place your Python logic here
#     return "Python script executed successfully!"
#
# if __name__ == '__main__':
#     app.run(debug=True)
#
# set1 = {1, 2, 3,4,6}
# set2 = {3, 4, 5}
# result = set1 | set2
# print(result)
# result = set1 & set2
# print(result)
# result = set2 ^ set1
# print(result)
# result = set1  - set2
# print(result)

import requests
api_url = "https://demo-dev.policypulse.io/Report/GetTimeSpentDetailsPerPageTopPercent?selectedDate=2025-01-09&selectedEndDate=2025-01-10&LOB=BusinessOwners&pageName=BuildingClassificationCoverages&Percentile=10&chartTitle=Average%20Time%20Spent%20Per%20Page"
hdrs = {
    "Authorization": "YOUR_API_KEY",
    "Content-Type": "application/json"
}

response= requests.get(api_url, headers=hdrs)

print(f"Status Code: {response.status_code}")

# Debugging: Print response content to check if it's JSON
print("Response Content:", response.text)
try:
    data = response.json()  # Try parsing JSON
    for assistant in data.get("assistants", []):  # Adjust based on API response structure
        print(f"Assistant ID: {assistant.get('id')}, Associated Page: {assistant.get('page_url')}")
except requests.exceptions.JSONDecodeError:
    print("Error: Response is not in JSON format. Check the API endpoint and response content.")