from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Initialize Chrome WebDriver
driver = webdriver.Chrome(service=Service())
driver.get("https://www.saucedemo.com")

# Login actions
driver.find_element(By.XPATH, '//*[@id="user-name"]').click()
driver.find_element(By.XPATH, '//*[@id="user-name"]').send_keys("standard_user")
driver.find_element(By.XPATH, '//*[@id="password"]').click()
driver.find_element(By.XPATH, '//*[@id="password"]').send_keys("secret_sauce")
driver.find_element(By.XPATH, '//*[@id="login-button"]').click()

# Navigation and interactions after login
driver.find_element(By.XPATH, '//*[@id="item_4_title_link"]/DIV[1]').click()
driver.find_element(By.XPATH, '//*[@id="add-to-cart"]').click()
driver.find_element(By.XPATH, '//*[@id="shopping_cart_container"]/A[1]').click()
driver.find_element(By.XPATH, '//*[@id="checkout"]').click()

# Checkout form filling
driver.find_element(By.XPATH, '//*[@id="first-name"]').click()
driver.find_element(By.XPATH, '//*[@id="first-name"]').send_keys("Vishnu")
driver.find_element(By.XPATH, '//*[@id="last-name"]').click()
driver.find_element(By.XPATH, '//*[@id="last-name"]').send_keys("Nandurkar")
driver.find_element(By.XPATH, '//*[@id="postal-code"]').click()
driver.find_element(By.XPATH, '//*[@id="postal-code"]').send_keys("92092")
driver.find_element(By.XPATH, '//*[@id="continue"]').click()
driver.find_element(By.XPATH, '//*[@id="finish"]').click()

# Final sleep
time.sleep(2)
driver.quit()