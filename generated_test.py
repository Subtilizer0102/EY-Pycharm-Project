from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome(service=Service())
driver.get("https://www.amazon.in/ap/register?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.in%2F%3Fref_%3Dnav_ya_signin&prevRID=0FFRJ6D8EV6SJRKN3TBW&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=inflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0")

wait = WebDriverWait(driver, 10)

name_input = wait.until(EC.presence_of_element_located((By.ID, "ap_customer_name")))
name_input.send_keys("Test User")

phone_input = wait.until(EC.presence_of_element_located((By.ID, "ap_phone_number")))
phone_input.send_keys("9876543210")

password_input = wait.until(EC.presence_of_element_located((By.ID, "ap_password")))
password_input.send_keys("Test@1234")

continue_button = wait.until(EC.element_to_be_clickable((By.ID, "continue")))
continue_button.click()

time.sleep(2)
time.sleep(5)
driver.quit()