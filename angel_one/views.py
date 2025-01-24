from rest_framework.views import APIView
from django.http import JsonResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import uuid
import os

# In-memory store for session and drivers
driver_store = {}

class StartangleLogin(APIView):
    def post(self, request):
        mobile_number = request.data.get("mobile_number")
        if not mobile_number:
            return JsonResponse({"error": "Mobile number is required."}, status=400)

        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        # Removing headless mode for debugging
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--remote-debugging-port=9222")

        chrome_prefs = {
            "download.default_directory": "/tmp",  # Set a writable directory for downloads
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
        }
        chrome_options.add_experimental_option("prefs", chrome_prefs)

        # Get the path to the ChromeDriver dynamically from the script's directory
        driver_path = ChromeDriverManager().install()
        service = Service(driver_path)

        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.maximize_window()
        try:
            driver.get("https://www.angelone.in/login/")

            email_input = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="mobile"]'))
            )
            email_input.send_keys(mobile_number)
            continue_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div/div[2]/form/button'))
            )
            continue_button.click()

            # Save session and return response
            session_id = str(uuid.uuid4())
            driver_store[session_id] = driver
            return JsonResponse({"message": "OTP required", "session_id": session_id})
        except Exception as e:
            driver.quit()
            return JsonResponse({"error": f"Failed to login: {str(e)}"}, status=500)

class ProvideOTPAngle(APIView):
    def post(self, request):
        session_id = request.data.get("session_id")
        otp = request.data.get("otp")
        pin = request.data.get("pin")
        from_date = request.data.get("From_Date")
        to_date = request.data.get("To_Date")

        if not session_id or not otp:
            return JsonResponse({"error": "Session ID and OTP are required."}, status=400)

        driver = driver_store.get(session_id)
        if not driver:
            return JsonResponse({"error": "Session expired or not found."}, status=400)

        try:
            otp_input = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="verifyOtp"]'))
            )
            otp_input.send_keys(otp)
            otp_input.send_keys(Keys.RETURN)

            pin_input = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="loginpin"]'))
            )
            pin_input.send_keys(pin)
            pin_input.send_keys(Keys.RETURN)

            got_it_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="modal"]/div/div/div[2]/button'))
            )
            got_it_button.click()

            not_now_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="modal"]/div/div[2]/div[2]/button[1]'))
            )
            not_now_button.click()

            profile_click = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="appContainer"]/div[2]/nav/nav/div/div[8]/div[1]/span'))
            )
            profile_click.click()

            reports = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="appContainer"]/div[3]/div[2]/div/div[2]/div[1]/div[2]/div[2]/div/div/div[2]/a[4]/div/div[2]/div/h3'))
            )
            reports.click()

            driver.switch_to.window(driver.window_handles[-1])
            from_date_input = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="customStartDatePNL"]'))
            )
            from_date_input.clear()
            from_date_input.send_keys(from_date)

            to_date_input = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="customEndDatePNL"]'))
            )
            to_date_input.clear()
            to_date_input.send_keys(to_date)

            download_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="download-reports-download-button"]'))
            )
            download_button.click()

            return JsonResponse({"status": "Success"}, status=200)
        except Exception as e:
            return JsonResponse({"error": f"Failed to provide OTP or generate report: {str(e)}"}, status=500)

