from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

LOGIN_URL = "https://brokersnapshot.com/LogIn"
SEARCH_URL = "https://brokersnapshot.com/?search="

# Use your actual login credentials
USERNAME = "shahrukhfiaz@gmail.com"
PASSWORD = "Saferfmcsa123@"

session = requests.Session()

def login_to_brokersnapshot():
    payload = {
        "email": USERNAME,
        "password": PASSWORD
    }

    # Custom headers
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0"
    }

    # Perform login
    login_response = session.post(LOGIN_URL, data=payload, headers=headers)
    return login_response.ok

@app.route('/get-name', methods=['GET'])
def get_name():
    usdot = request.args.get('usdot')

    if not usdot:
        return jsonify({"error": "Missing 'usdot' parameter"}), 400

    # Login first
    if not login_to_brokersnapshot():
        return jsonify({"error": "Failed to login"}), 401

    # Search the USDOT
    search_response = session.get(SEARCH_URL + usdot)
    soup = BeautifulSoup(search_response.text, 'html.parser')

    # Extract full name from result
    try:
        lead_name_tag = soup.find("span", class_="MuiTypography-root MuiTypography-h5 css-1b4e4nt")
        if not lead_name_tag:
            return jsonify({"error": "Name not found"}), 404

        lead_name = lead_name_tag.text.strip()
        return jsonify({"usdot": usdot, "name": lead_name})

    except Exception as e:
        return jsonify({"error": "Parsing failed", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
