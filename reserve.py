from selenium import webdriver
from selenium.webdriver.common.by import By
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from login import patch_reef_login
import requests
import datetime
import pytz
import json 
from bs4 import BeautifulSoup
from datetime import timedelta



driver = webdriver.Chrome()

def check_availability(driver):
    print("Checking availability...")
    now = datetime.datetime.now()
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    eastern = pytz.timezone('US/Eastern')
    midnight = eastern.localize(midnight)
    tomorrow_midnight = midnight + timedelta(days=1)
    # Convert it to a Unix timestamp
    timestamp = int(tomorrow_midnight.timestamp())
    url = f"https://playbycourt.com/api/facilities/73/available_hours?timestamp={timestamp}&surface=pickleball&kind=reservation"
    driver.get(url)
    response = driver.page_source
    soup = BeautifulSoup(response, 'html.parser')
    pre_tag = soup.find('pre')
    json_text = pre_tag.text
    data = json.loads(json_text)

    available_hours = [slot for slot in data['available_hours'] if slot['available']]
    return available_hours


def book_court(driver):
    # Interact with the page to book the court
    # Check whether booking was successful
    # Return True if successful, False if not
    pass
def send_email():
    # Set up SMTP client with your email server
    # Login to your email account
    # Create message using MIMEMultipart and MIMEText
    # Send email    
    pass
def main():
    # Instantiate a ChromeDriver
    driver = webdriver.Chrome()
    patch_reef_login(driver)
    print("Logged in")
    availability = check_availability(driver=driver)
    print(availability)


    # Close the driver after use
    driver.close()

if __name__ == "__main__":
    main()
