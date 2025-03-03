from rest_framework.views import APIView
from django.http import JsonResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import uuid
import time
import os

# A simple in-memory store for demonstration purposes (not suitable for production)
driver_store = {}

# Function to create a new Chrome WebDriver instance
def create_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--remote-debugging-port=9222")

    # Set download preferences
    download_dir = os.path.abspath("downloads")  # Change this as needed
    os.makedirs(download_dir, exist_ok=True)
    chrome_prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", chrome_prefs)

    # Set up WebDriver
    service = Service(r"C:\Users\Sinewave#2022\Downloads\chromedriver-win64 (1)\chromedriver-win64\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.maximize_window()
    return driver

class StartGrowwLogin(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return JsonResponse({"error": "Email and password are required."}, status=400)

        driver = create_driver()

        try:
            driver.get("https://groww.in/login")
            wait = WebDriverWait(driver, 10)

            # Enter Email
            email_input = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="login_email1"]')))
            email_input.send_keys(email)

            # Click Continue
            continue_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="lils382InitialLoginScreen"]/div[3]/div[3]/button/span')))
            continue_button.click()

            # Enter Password
            password_input = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="login_password1"]')))
            password_input.send_keys(password)
            password_input.send_keys(Keys.RETURN)

            # Generate session ID
            session_id = str(uuid.uuid4())
            driver_store[session_id] = driver

            return JsonResponse({"message": "Please provide the OTP via /provide-otp endpoint.", "session_id": session_id})

        except Exception as e:
            driver.quit()
            return JsonResponse({"error": f"Login failed: {str(e)}"}, status=500)

class ProvideOTP(APIView):
    def post(self, request):
        session_id = request.data.get("session_id")
        otp = request.data.get("otp")
        pin = request.data.get("pin")

        if not session_id or not otp:
            return JsonResponse({"error": "Session ID and OTP are required."}, status=400)

        driver = driver_store.get(session_id)
        if not driver:
            return JsonResponse({"error": "Session not found or expired."}, status=400)

        try:
            wait = WebDriverWait(driver, 20)

            # Enter OTP
            otp_input = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[contains(@id, "otpinput")]')))
            otp_input.send_keys(otp)
            otp_input.send_keys(Keys.RETURN)
            time.sleep(2)

            # Enter PIN (if provided)
            if pin:
                pin_input = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[contains(@id, "pininput")]')))
                pin_input.send_keys(pin)
                pin_input.send_keys(Keys.RETURN)
                time.sleep(2)

            # Navigate to Reports
            erow = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div[1]/div/div/header/div[3]/div/div[2]/div[1]/div/div[2]')))
            erow.click()

            report_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="reports"]/div[2]/div[1]')))
            report_button.click()

            # Download Mutual Fund Capital Gain Report
            mutual_fund_capital_gain = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="profilePage"]/div/div/div/div/div[2]/div/div[1]/div[1]/div[2]/div[2]/div[2]')))
            mutual_fund_capital_gain.click()

            download_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="profilePage"]/div/div/div/div/div[2]/div/div[1]/div[2]/div[1]/div[3]/button/span')))
            download_button.click()

            # Download Stocks Capital Gain Report
            stocks_capital_gain = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="profilePage"]/div/div/div/div/div[2]/div/div[1]/div[1]/div[2]/div[2]/div[3]')))
            stocks_capital_gain.click()

            download_button_2 = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="profilePage"]/div/div/div/div/div[2]/div/div[1]/div[2]/div[1]/div[3]/button/span')))
            download_button_2.click()

            return JsonResponse({"message": "OTP processed successfully, downloads should proceed."})

        except Exception as e:
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)

