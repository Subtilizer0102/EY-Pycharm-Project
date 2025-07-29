from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
# Launch browser
driver = webdriver.Chrome()
driver.get("https://www.google.com")
# Accept cookies if popup appears
try:
    consent = driver.find_element(By.ID, "L2AGLb")
    consent.click()
except:
    pass  # No consent button shown
    #Enter text into search box
search_box = driver.find_element(By.NAME, "q")
search_box.send_keys("OpenAI")
search_box.send_keys(Keys.RETURN)  # Press Enter# Wait for results to load
time.sleep(10)
# Assert that results page contains the query
assert "OpenAI" in driver.title# Close browser
driver.quit()