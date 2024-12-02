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

# A simple in-memory store for demonstration purposes (not suitable for production)
driver_store = {}

class StartGrowwLogin(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        
        if not email or not password:
            return JsonResponse({"error": "Email and password are required."}, status=400)
        
        # Set up Chrome options for headless mode
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run Chrome in headless mode
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--remote-debugging-port=9222")
        
        # Configure for automatic downloads in headless mode
        download_dir = "path_to_your_download_directory"  # Change this to your desired directory
        chrome_prefs = {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }
        chrome_options.add_experimental_option("prefs", chrome_prefs)

        # Full path to the chromedriver binary
        service = Service('/home/ubuntu/Taxenv/mytaxbase_2/chromedriver')
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service=service, options=options)
                
        try:
            # Login process
            driver.get("https://groww.in/login")
            email_input = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="login_email1"]'))
            )
            email_input.send_keys(email)
            continue_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="lils382InitialLoginScreen"]/div[3]/div[3]/button/span'))
            )
            continue_button.click()
            password_input = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="login_password1"]'))
            )
            password_input.send_keys(password)
            password_input.send_keys(Keys.RETURN)

            # Generate session ID
            session_id = str(uuid.uuid4())
            driver_store[session_id] = driver  # Save driver in a temporary store

            return JsonResponse({"message": "Please provide the OTP via /provide-otp endpoint.", "session_id": session_id})

        except Exception as e:
            driver.quit()
            return JsonResponse({"error": str(e)}, status=500)

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
            # Enter OTP and proceed
            otp_input = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="otpinput88parent"]/div[1]/input'))
            )
            otp_input.send_keys(otp)
            otp_input.send_keys(Keys.RETURN)
            time.sleep(2)

            pin_input = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="otpinput88parent"]/div[1]/input'))
            )
            pin_input.send_keys(pin)
            pin_input.send_keys(Keys.RETURN)
            time.sleep(2)

            # Navigate and download mutual fund capital gain report
            erow = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div[1]/div/div/header/div[3]/div/div[2]/div[1]/div/div[2]'))
            )
            erow.click()

            report_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="reports"]/div[2]/div[1]'))
            )
            report_button.click()

            mutual_fund_capital_gain = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="profilePage"]/div/div/div/div/div[2]/div/div[1]/div[1]/div[2]/div[2]/div[2]'))
            )
            mutual_fund_capital_gain.click()

            download_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="profilePage"]/div/div/div/div/div[2]/div/div[1]/div[2]/div[1]/div[3]/button/span'))
            )
            download_button.click()

            # Download stocks capital gain report
            stocks_capital_gain = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="profilePage"]/div/div/div/div/div[2]/div/div[1]/div[1]/div[2]/div[2]/div[3]'))
            )
            stocks_capital_gain.click()

            download_button_2 = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="profilePage"]/div/div/div/div/div[2]/div/div[1]/div[2]/div[1]/div[3]/button/span'))
            )
            download_button_2.click()

            return JsonResponse({"message": "OTP processed successfully, downloads should proceed."})

        except Exception as e:
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)
