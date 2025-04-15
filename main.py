from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

USERNAME = "your_email@example.com"
PASSWORD = "your_password"
LOGIN_URL = "https://brokersnapshot.com/LogIn"
SEARCH_URL = "https://brokersnapshot.com/?search="

def scrape_full_name(usdot):
    session = requests.Session()

    # 1. Log in to BrokerSnapshot
    login_payload = {
        "email": USERNAME,
        "password": PASSWORD
    }

    login_headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    login_response = session.post(LOGIN_URL, data=login_payload, headers=login_headers)

    if login_response.status_code != 200 or "Dashboard" not in login_response.text:
        return {"error": "Login failed", "status_code": login_response.status_code}

    # 2. Search with USDOT
    search_response = session.get(f"{SEARCH_URL}{usdot}")

    if search_response.status_code != 200:
        return {"error": "Search request failed"}

    soup = BeautifulSoup(search_response.text, "html.parser")

    # Adjust selector based on actual page structure
    name_element = soup.find("h4", class_="company-name")

    if not name_element:
        return {"usdot": usdot, "full_name": None, "error": "Company name not found"}

    return {
        "usdot": usdot,
        "full_name": name_element.text.strip()
    }

@app.route("/scrape", methods=["GET"])
def scrape():
    usdot = request.args.get("usdot")
    if not usdot:
        return jsonify({"error": "USDOT number is required"}), 400

    result = scrape_full_name(usdot)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
