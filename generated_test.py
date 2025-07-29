from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
driver.get("https://www.saucedemo.com")

try:
    username = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "user-name")))
    username.send_keys("standard_user")
    password = driver.find_element(By.ID, "password")
    password.send_keys("secret_sauce")
    login_button = driver.find_element(By.ID, "login-button")
    login_button.click()

    inventory_container = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "inventory_container")))
    add_to_cart_button = driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack")
    add_to_cart_button.click()

    cart_badge = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "shopping_cart_badge")))
    cart_icon = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
    cart_icon.click()

    checkout_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "checkout")))
    checkout_button.click()

    checkout_form = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "checkout_info_container")))
    first_name = driver.find_element(By.ID, "first-name")
    first_name.send_keys("John")
    last_name = driver.find_element(By.ID, "last-name")
    last_name.send_keys("Doe")
    postal_code = driver.find_element(By.ID, "postal-code")
    postal_code.send_keys("12345")
    continue_button = driver.find_element(By.ID, "continue")
    continue_button.click()

    finish_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "finish")))
    finish_button.click()

    time.sleep(2)
    time.sleep(5)
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    driver.quit()