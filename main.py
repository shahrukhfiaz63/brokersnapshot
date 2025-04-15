from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

LOGIN_URL = "https://brokersnapshot.com/LogIn"
SEARCH_URL = "https://brokersnapshot.com/?search="
USERNAME = "shahrukhfiaz@gmail.com"
PASSWORD = "Saferfmcsa123@"

session = requests.Session()

def login():
    # Initial GET to grab cookies if needed
    session.get(LOGIN_URL)
    
    payload = {
        "email": USERNAME,
        "password": PASSWORD
    }

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = session.post(LOGIN_URL, data=payload, headers=headers)
    return response.ok

def get_broker_name(usdot):
    if not login():
        return {"error": "Login failed"}

    search_url = f"{SEARCH_URL}{usdot}"
    res = session.get(search_url)

    if res.status_code != 200:
        return {"error": "Failed to fetch broker data"}

    soup = BeautifulSoup(res.text, "html.parser")

    # Attempt to find the full name based on layout — adjust as needed
    name_element = soup.find("h2")  # This depends on how the site structures the result
    if name_element:
        return {
            "usdot": usdot,
            "broker_name": name_element.text.strip()
        }
    else:
        return {
            "usdot": usdot,
            "broker_name": "Not Found"
        }

@app.route("/broker", methods=["GET"])
def broker_lookup():
    usdot = request.args.get("usdot")
    if not usdot:
        return jsonify({"error": "Missing USDOT number"}), 400

    try:
        result = get_broker_name(usdot)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": "Exception occurred", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
