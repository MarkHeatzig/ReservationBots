from selenium import webdriver
import selenium
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
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from constants import USERNAME, PASSWORD
import pandas as pd
from selenium.webdriver.chrome.options import Options


# Define the columns for your DataFrame
columns = ['Sport', 'Team', 'Product ID', 'Product Name', 'Product Price', 'Brand Name', 'Product URL']
rows = []

driver = webdriver.Chrome()

def back_home(driver, sport):
    driver.get('https://www.fanatics.com')
    sport_logo = WebDriverWait(driver, 25).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, f'a[data-trk-id="primary-selector-{sport}"]'))
    )
    sport_logo.click()
    return ''


def check_products(driver):
    
    
    # Create the DataFrame
    df = pd.DataFrame(columns=columns)


    # break_dict = {"NFL":32, "MLB": 50, "NBA": 50, "MLS": 50, "Soccer": 48}
    # sports = ["NFL", "MLB", "NBA", "MLS", "Soccer"]


    # break_dict = {"MLB": 50, "NBA": 50, "MLS": 50, "Soccer": 48}
    # sports = ["MLB", "NBA", "MLS", "Soccer"]

    # break_dict = {"NHL": 50, "Soccer": 48}
    # sports = ["NHL", "Soccer"]

    break_dict = {"NCAA": 50}
    sports = ["NCAA"]

    for sport in sports:
        print("We are on sport: ", sport)
        driver.get('https://www.fanatics.com')
        rows = []
        sport_logo = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f'a[data-trk-id="primary-selector-{sport}"]'))
        )
        sport_logo.click()
        sleep(1)
        source = driver.page_source
        soup = BeautifulSoup(source, 'html.parser')
        secondary_selector_items = soup.find_all(class_='secondary-selector-item')
        i=0
        for item in secondary_selector_items:
            print('We are on item: ', i, ' of ', len(secondary_selector_items))
            i+=1
            if i == break_dict[sport]:
                break
            data_trk_id = item.a['data-trk-id']
            print(data_trk_id)
            sleep(3)
            try:
                team_link = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, f'a[data-trk-id="{data_trk_id}"]'))
                )
                team_link.click()
                sleep(3)
            except selenium.common.exceptions.TimeoutException:
                print(f"No 'team' link found for {data_trk_id}. Continuing to next item.")
                back_home(driver, sport)

                continue

            try:
                baby_link = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'a[data-trk-id="baby"]'))
                )
                baby_link.click()
                sleep(3)
            except selenium.common.exceptions.TimeoutException:
                print(f"No 'baby' link found for {data_trk_id}. Continuing to next item.")
                back_home(driver, sport)

                continue


            soup = BeautifulSoup(driver.page_source, 'html.parser')

            script_tag = soup.find('script', {'type': 'application/ld+json'})
            product_listing_data = json.loads(script_tag.string)

            for product in product_listing_data:
                # Extract the required information
                product_name = product.get('name')
                product_id = product['offers'][0].get('serialNumber')
                product_price = product['offers'][0]['priceSpecification'].get('price')
                url = product.get('url')
                brand_name = product.get('brand')
                new_row = [sport, data_trk_id, product_id, product_name, product_price, brand_name, url]
                rows.append(new_row)
            df = pd.DataFrame(rows, columns=columns)
            df.to_csv(f"{sport}_output.csv", index=False)
            back_home(driver, sport)
            
        print('Finished with sport: ', sport)

    return rows

def main():
    # Instantiate a ChromeDriver
    options = Options()
    # options.add_argument('--headless')
    # options.add_argument('--window-size=1920x1080')

    driver = webdriver.Chrome()
    result = check_products(driver=driver)
    df = pd.DataFrame(result, columns=columns)
    # Save DataFrame to Excel
    df.to_excel("output.xlsx", index=False)
        
    # Close the driver after use
    driver.close()

if __name__ == "__main__":
    main()
