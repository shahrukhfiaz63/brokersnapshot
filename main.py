from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

USERNAME = "shahrukhfiaz@gmail.com"
PASSWORD = "Saferfmcsa123@"
LOGIN_URL = "https://brokersnapshot.com/LogIn"
SEARCH_URL = "https://brokersnapshot.com/?search="

session = requests.Session()

def login():
    payload = {
        "username": USERNAME,
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

    response = session.get(SEARCH_URL + usdot)
    if response.status_code != 200:
        return {"error": "Search failed", "status": response.status_code}

    soup = BeautifulSoup(response.text, "html.parser")
    result = soup.find("h2", class_="text-dark")

    if result:
        return {"usdot": usdot, "broker_name": result.text.strip()}
    else:
        return {"usdot": usdot, "broker_name": None}

@app.route("/broker", methods=["GET"])
def broker_lookup():
    usdot = request.args.get("usdot")
    if not usdot:
        return jsonify({"error": "Missing USDOT number"}), 400

    return jsonify(get_broker_name(usdot))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
