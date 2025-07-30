from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize the driver
driver = webdriver.Chrome(service=Service())
driver.get("https://www.saucedemo.com")

# Wait for the page to load and elements to be present
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "user-name")))

# Fill in username and password
driver.find_element(By.ID, "user-name").send_keys("test_user")
driver.find_element(By.ID, "password").send_keys("test_password")

# Click the login button
driver.find_element(By.ID, "login-button").click()

# Wait for the next page to load or perform further actions
WebDriverWait(driver, 10).until(EC.url_to_be("https://www.saucedemo.com/inventory.html"))

time.sleep(5)
driver.quit()