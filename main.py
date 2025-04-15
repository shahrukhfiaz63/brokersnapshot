import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify

app = Flask(__name__)

# Replace these with your actual BrokerSnapshot credentials
USERNAME = 'your_email@example.com'
PASSWORD = 'your_password'
LOGIN_URL = 'https://brokersnapshot.com/login'
SEARCH_URL = 'https://brokersnapshot.com/?search='

def get_csrf_token(session, url):
    """Extract CSRF token from login page"""
    response = session.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    token_input = soup.find('input', {'name': '_token'})
    return token_input['value'] if token_input else None

def scrape_full_name(usdot):
    with requests.Session() as session:
        csrf_token = get_csrf_token(session, LOGIN_URL)

        if not csrf_token:
            return {'error': 'CSRF token not found'}

        # Log in to the site
        login_payload = {
            'email': USERNAME,
            'password': PASSWORD,
            '_token': csrf_token
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        login_response = session.post(LOGIN_URL, data=login_payload, headers=headers)

        if login_response.status_code != 200:
            return {'error': 'Login failed', 'status': login_response.status_code}

        # Search using the USDOT number
        search_url = f"{SEARCH_URL}{usdot}"
        search_response = session.get(search_url)

        soup = BeautifulSoup(search_response.text, 'html.parser')

        # Adjust selector based on BrokerSnapshot HTML structure
        # Example: <h4 class="company-name">XYZ Logistics LLC</h4>
        name_element = soup.find('h4', class_='company-name')

        if not name_element:
            return {'error': 'Name not found'}

        return {
            'usdot': usdot,
            'full_name': name_element.text.strip()
        }

@app.route('/scrape', methods=['GET'])
def scrape():
    usdot = request.args.get('usdot')
    if not usdot:
        return jsonify({'error': 'USDOT not provided'}), 400

    result = scrape_full_name(usdot)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
