from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get("https://www.saucedemo.com/")

username = driver.find_element(By.ID, "user-name")
password = driver.find_element(By.ID, "password")
login_button = driver.find_element(By.ID, "login-button")
username.send_keys("standard_user")
password.send_keys("secret_sauce")
login_button.click()

backpack = driver.find_element(By.ID, "item_4_title_link")
backpack.click()

add_cart = driver.find_element(By.ID, "add-to-cart")
add_cart.click()

cart_link = driver.find_element(By.ID, "shopping_cart_container")
cart_link.click()

checkout = driver.find_element(By.ID, "checkout")
checkout.click()

first_name = driver.find_element(By.ID, "first-name")
first_name.click()
first_name.send_keys("Vishnu")

last_name = driver.find_element(By.ID, "last-name")
last_name.click()
last_name.send_keys("Nandurkar")

zip_element = driver.find_element(By.ID, "postal-code")
zip_element.click()
zip_element.send_keys("400051")

continue_button = driver.find_element(By.ID, "continue")
continue_button.click()

finish_button = driver.find_element(By.ID, "finish")
finish_button.click()

time.sleep(10)
driver.quit()