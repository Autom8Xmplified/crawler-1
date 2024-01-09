from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
import time, base64, os


chrome_options = webdriver.ChromeOptions()
service = Service(executable_path=os.environ.get("CHROMEDRIVER_PATH"))
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
browser = webdriver.Chrome(service=service, options=chrome_options)

def Fill_Form(url, contact_person, contact_number, street, email, city, loanNumber, state, zip, inspectionDateTime, InspectorName, Summary):
    browser.get(url)
    browser.implicitly_wait(15)
    try:
        try:
            StartFill_btn = browser.find_element(By.CLASS_NAME, "js-pdfStartFilling")
            StartFill_btn.click()
            browser.implicitly_wait(15)
        except NoSuchElementException:
            pass
        browser.find_element(By.ID, "input_2").send_keys(contact_person)
        browser.find_element(By.ID, "input_3").send_keys(contact_number)
        browser.find_element(By.ID, "input_4").send_keys(street)
        browser.find_element(By.ID, "input_5").send_keys(email)
        browser.find_element(By.ID, "input_6").send_keys(city)
        browser.find_element(By.ID, "input_7").send_keys(loanNumber)
        browser.find_element(By.ID, "input_8").send_keys(state)
        browser.find_element(By.ID, "input_9").send_keys(zip)
        browser.find_element(By.ID, "input_18").send_keys(inspectionDateTime)
        browser.find_element(By.ID, "input_14").send_keys(InspectorName)
        browser.find_element(By.ID, "input_11").send_keys(Summary)

        #Scroll down to find the Buttons
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        return "completed"

    except NoSuchElementException:
        return "failed"

def Preview():
     # Perform Preview Mode
    Preview_PDF = browser.find_element(By.ID, "input_preview_12")
    Preview_PDF.click()
    browser.implicitly_wait(25)
    try:
        time.sleep(10)
        image = browser.find_element(By.CLASS_NAME, 'react-pdf__Page__canvas');
        canvas_64 = browser.execute_script("return arguments[0].toDataURL('image/png').substring(22);", image)
        # decode
        decode = base64.b64decode(canvas_64)
        with open(r"canvas.png", "wb") as f:
            f.write(decode)
        return canvas_64
    except NoSuchElementException:
        print("Element is not found")
        browser.quit()
        return 'failed'

def Submit():
    try: 
        Preview_PDF = browser.find_element(By.ID, "input_12")
        Preview_PDF.click()
        return "submitted"
        browser.quit()
    except Exception:
        browser.quit()
        return "failed"
