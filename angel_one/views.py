from rest_framework.views import APIView
from django.http import JsonResponse, FileResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import uuid
import os

# In-memory store for session and WebDriver instances
driver_store = {}

# Configure download directory for the headless browser
DOWNLOAD_DIR = "/tmp"  # Path on the server
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

class StartangleLogin(APIView):
    def post(self, request):
        mobile_number = request.data.get("mobile_number")
        if not mobile_number:
            return JsonResponse({"error": "Mobile number is required."}, status=400)

        # Configure Chrome options for headless mode
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--remote-debugging-port=9222")
        chrome_options.add_experimental_option("prefs", {
            "download.default_directory": DOWNLOAD_DIR,
            "download.prompt_for_download": False,
            "safebrowsing.enabled": True
        })

        # Set up WebDriver
        service = Service("/usr/local/bin/chromedriver")  # Ensure the path to ChromeDriver is correct
        driver = webdriver.Chrome(service=service, options=chrome_options)

        try:
            driver.get("https://www.angelone.in/login/")
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="mobile"]'))
            ).send_keys(mobile_number)

            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div/div[2]/form/button'))
            ).click()

            # Save session and driver
            session_id = str(uuid.uuid4())
            driver_store[session_id] = driver
            return JsonResponse({"message": "OTP required", "session_id": session_id})
        except Exception as e:
            driver.quit()
            return JsonResponse({"error": f"Failed to initiate login: {str(e)}"}, status=500)


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
            # Enter OTP
            WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="verifyOtp"]'))
            ).send_keys(otp, Keys.RETURN)

            # Enter PIN
            WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="loginpin"]'))
            ).send_keys(pin, Keys.RETURN)

            # Handle modals and navigate to reports
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="modal"]/div/div/div[2]/button'))
            ).click()

            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="modal"]/div/div[2]/div[2]/button[1]'))
            ).click()

            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="appContainer"]/div[2]/nav/nav/div/div[8]/div[1]/span'))
            ).click()

            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="appContainer"]/div[3]/div[2]/div/div[2]/div[1]/div[2]/div[2]/div/div/div[2]/a[4]/div/div[2]/div/h3'))
            ).click()

            # Switch to new tab and enter date range
            driver.switch_to.window(driver.window_handles[-1])
            WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="customStartDatePNL"]'))
            ).send_keys(from_date)

            WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="customEndDatePNL"]'))
            ).send_keys(to_date)

            # Click download button
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="download-reports-download-button"]'))
            ).click()

            return JsonResponse({"status": "Success", "message": "Report download initiated."}, status=200)
        except Exception as e:
            return JsonResponse({"error": f"Failed to process OTP and download reports: {str(e)}"}, status=500)



    class DownloadFile(APIView):
        def get(self, request):
            # Get the list of all files in the download directory
            files = sorted(
                [(f, os.path.getmtime(os.path.join(DOWNLOAD_DIR, f))) for f in os.listdir(DOWNLOAD_DIR)],
                key=lambda x: x[1], reverse=True
            )

            # Fetch the last file
            if len(files) < 1:
                return JsonResponse({"error": "No files available for download."}, status=400)

            latest_file = os.path.join(DOWNLOAD_DIR, files[0][0])
            try:
                filename = os.path.basename(latest_file)
                response = FileResponse(open(latest_file, "rb"), as_attachment=True, filename=filename)
                return JsonResponse({
                    "status": "Success",
                    "message": "File downloaded successfully.",
                    "filename": filename
                }, status=200)
            except Exception as e:
                return JsonResponse({"error": f"Error during file download: {str(e)}"}, status=500)