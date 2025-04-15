from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

app = Flask(__name__)

def get_company_name(usdot):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.binary_location = "/usr/bin/chromium"

    driver = webdriver.Chrome(options=options)

    try:
        # 1. Log in
        driver.get("https://brokersnapshot.com/LogIn")
        time.sleep(2)

        driver.find_element(By.ID, "email").send_keys("shahrukhfiaz@gmail.com")
        driver.find_element(By.ID, "password").send_keys("Saferfmcsa123@")
        driver.find_element(By.ID, "ok-button").click()
        time.sleep(3)

        # 2. Search USDOT
        driver.get(f"https://brokersnapshot.com/?search={usdot}")
        time.sleep(3)

        # 3. Extract company name
        company_elem = driver.find_element(By.XPATH, "//td[@data-label='Company']//a")
        return {"usdot": usdot, "company_name": company_elem.text.strip()}

    except Exception as e:
        return {"error": str(e)}

    finally:
        driver.quit()

@app.route('/get-name', methods=['GET'])
def get_name():
    usdot = request.args.get('usdot')
    if not usdot:
        return jsonify({"error": "Missing 'usdot' parameter"}), 400

    result = get_company_name(usdot)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
