from rest_framework.views import APIView
from django.http import JsonResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import uuid
import time

# A simple in-memory store for demonstration purposes (not suitable for production)
driver_store = {}

class StartICICIDirectLogin(APIView):
    def post(self, request):
        number = request.data.get("number")
        password = request.data.get("password")
        
        if not number or not password:
            return JsonResponse({"error": "Number and password are required."}, status=400)

        # Set up WebDriver (modify the path to ChromeDriver as needed)
        service = Service(r"C:\Users\Sinewave#2022\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe")
        driver = webdriver.Chrome(service=service)
        driver.maximize_window()

        try:
            # Navigate to ICICI Direct login page
            driver.get("https://secure.icicidirect.com/customer/login")

            # Enter number (user ID)
            email_input = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="txtu"]'))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", email_input)  # Scroll into view if needed
            email_input.click()
            email_input.send_keys(number)

            print("Number entered successfully")

            # Enter password
            password_input = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="txtp"]'))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", password_input)  # Scroll into view
            password_input.click()  # Optional click to focus if needed
            password_input.send_keys(password)
            password_input.send_keys(Keys.RETURN)

            print("Password entered successfully")

            # # Click continue button
            # continue_button = WebDriverWait(driver, 10).until(
            #     EC.element_to_be_clickable((By.XPATH, '//*[@id="btnlogin"]'))
            # )
            # continue_button.click()

            # print("Continue button clicked")

            # Generate and return a session ID using UUID for uniqueness
            session_id = str(uuid.uuid4())  # More secure and unique session ID
            driver_store[session_id] = driver  # Save driver in a temporary store

            return JsonResponse({"message": "Please provide the OTP via /provide-otp endpoint.", "session_id": session_id})

        except Exception as e:
            driver.quit()
            return JsonResponse({"error": str(e)}, status=500)





class ProvideOTPICICIDirect(APIView):
    def post(self, request):
        session_id = request.data.get("session_id")
        otp = request.data.get("otp")
       
        if not session_id or not otp:
            return JsonResponse({"error": "Session ID and OTP are required."}, status=400)

        # Retrieve the driver instance from the store
        driver = driver_store.get(session_id)
        if not driver:
            return JsonResponse({"error": "Session not found or expired."}, status=400)

        try:
            # Step 1: Locate and interact with OTP input
            otp_input = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="frmotp"]/div/div[4]/div/div[1]/input'))
            )
            otp_input.clear()
            otp_input.send_keys(otp)
            otp_input.send_keys(Keys.RETURN)
            time.sleep(5)


            # Step 3: Handle the "Got it" button
            got_it_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="pnlmnudsp"]/div[1]/div/ul/li[1]/a'))
            )
            got_it_button.click()
            time.sleep(5)
         

            # Step 4: Handle the "Not now" button
            not_now_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="frm"]/div[2]/div[2]/div/div/ul/li[1]/a'))
            )
            not_now_button.click()
            time.sleep(5)

               #----------------------------------

            # # Step 5: Click on profile
            # profile_click = WebDriverWait(driver, 10).until(
            #     EC.element_to_be_clickable((By.XPATH, '//*[@id="account-nav-items"]/ul/li[1]/a'))
            # )
            # profile_click.click()
            # time.sleep(5)

            # # Step 7: Switch to the new tab
            # window_handles = driver.window_handles
            # driver.switch_to.window(window_handles[-1])  # Switch to the last opened tab (new tab)

            # # Step 6: Click on reports
            # reports = WebDriverWait(driver, 10).until(
            #     EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div[1]/div/div/div[1]/a[3]/span'))
            # )
            # reports.click()
            # time.sleep(5)  # Wait for the new tab to open

            

            # # Step 8: Wait for and interact with the "From Date" input
            # from_date_input = WebDriverWait(driver, 20).until(
            #     EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div[1]/div/div/div[1]/div/ul/li[5]/a/span'))
            # )
            # from_date_input.click()
            # time.sleep(5)  # Wait for the new tab to open

            # # Step 10: Click the download button
            # download_button = WebDriverWait(driver, 10).until(
            #     EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div[2]/div/div/div/div[1]/form/div/div[1]/select'))
            # )
            # download_button.click()
            # time.sleep(5)  # Allow time for the download to start


            #             # Step 10: Click the download button
            # download_R = WebDriverWait(driver, 10).until(
            #     EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div[2]/div/div/div/div[1]/form/div/div[1]/select/option[6]'))
            # )
            # download_R.click()
            # time.sleep(5)  # Allow time for the download to start


            # download_B = WebDriverWait(driver, 10).until(
            #     EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div[2]/div/div/div/div[1]/form/div/div[3]/button'))
            # )
            # download_B.click()
            # time.sleep(5)  # Allow time for the download to start

            return JsonResponse({"status": "Success"}, status=200)

        except Exception as e:
            # Handle exceptions and provide an error response
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)