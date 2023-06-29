from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from constants import USERNAME, PASSWORD

def patch_reef_login(driver):
    print("Logging in...")
    # Navigate to the login page
    driver.get("https://playbycourt.com/book/patch-reef-park-tennis-center")

    # Wait for the input fields to be loaded
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "user_email"))
    )
    print("Email field loaded")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "user_password"))
    )
    print("Password field loaded")
    # Fill the username
    username_field = driver.find_element(By.ID, "user_email")
    username_field.send_keys(USERNAME)
    sleep(2)
    # Fill the password
    password_field = driver.find_element(By.ID, "user_password")
    password_field.send_keys(PASSWORD)

    # Submit the form
    driver.find_element(By.NAME, "commit").click()
