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
columns = ['Sport', 'Team', 'Product ID', 'Product Name', 'Product Price']
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
    driver.get('https://www.fanatics.com')
    
    # Create the DataFrame
    df = pd.DataFrame(columns=columns)
    print(type(df))
    dataframe = df
    # break_dict = {"NFL":32, "MLB": 50, "NBA": 50, "MLS": 50, "Soccer": 48}
    # sports = ["NFL", "MLB", "NBA", "MLS", "Soccer"]
    # break_dict = {"MLB": 50, "NBA": 50, "MLS": 50, "Soccer": 48}
    # sports = ["MLB", "NBA", "MLS", "Soccer"]

    # break_dict = {"NBA": 50, "MLS": 50, "Soccer": 48}
    # sports = ["NBA", "MLS", "Soccer"]
    break_dict = {"NHL": 48}
    sports = ["NHL"]

    for sport in sports:
        rows = []
        sport_logo = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f'a[data-trk-id="primary-selector-{sport}"]'))
        )
        sport_logo.click()
        sleep(2)
        source = driver.page_source
        soup = BeautifulSoup(source, 'html.parser')
        secondary_selector_items = soup.find_all(class_='secondary-selector-item')
        i=0
        for item in secondary_selector_items:
            i+=1
            if i == break_dict[sport]:
                break
            print('We are on item: ', i, ' of ', len(secondary_selector_items))
            data_trk_id = item.a['data-trk-id']
            print(data_trk_id)
            sleep(1)

            team_link = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, f'a[data-trk-id="{data_trk_id}"]'))
            )
            team_link.click()
            sleep(1)
            try:
                baby_link = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'a[data-trk-id="baby"]'))
                )
                baby_link.click()
                sleep(1)
            except selenium.common.exceptions.TimeoutException:
                print(f"No 'baby' link found for {data_trk_id}. Continuing to next item.")
                continue

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            product = soup.find('div', class_='grid-small-1-medium-3 row small-up-1 medium-up-3')

            product_containers = soup.find_all('div', class_='product-card row')
            for product in product_containers:
                try:
                    # find the product title element
                    product_title_element = product.find('div', class_='product-card-title').find('a')
                    
                    # extract product ID
                    product_id = product_title_element.get('data-trk-id')
                    print(f'Product ID: {product_id}')
                    
                    # extract product name
                    product_name = product_title_element.text.strip()
                    print(f'Product Name: {product_name}')
                    
                    # extract product price
                    product_price_element = product.find('div', class_='price-card').find('span', class_='sr-only')
                    if product_price_element is not None:
                        product_price = product_price_element.text.strip()
                        print(f'Product Price: {product_price}\n')
                    else:
                        print('Product Price: Not found\n')
                    new_row = [sport, data_trk_id, product_id, product_name, product_price]
                    rows.append(new_row)
                    df = pd.DataFrame(rows, columns=columns)
                    df.to_csv(f"{sport}_output.csv", index=False)
                except selenium.common.exceptions.TimeoutException:
                    print(f"TimeoutException for {data_trk_id}. Continuing to next item.")
                    continue
            back_home(driver, sport)
        print('We are saving the following DataFrame to a CSV file: \n')
        back_home(driver, sport)

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
