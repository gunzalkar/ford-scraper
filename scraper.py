import time
import csv
import os
import pandas as pd
import urllib.request as req
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException

# Setting up the Chrome webdriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

def scrape_data(zip_code):
    # Format zip code to ensure it has leading zeros
    formatted_zip = f'{zip_code:05d}'
    url = f'https://www.ford.com/dealerships/#/q/{formatted_zip}/radius/50'
    driver.get(url)
    while True:
        try:
            view_more_button = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH, "//button[contains(., 'View More Dealers')]")))
            view_more_button.click()
            time.sleep(2)
        except:
            break

    # error_element = driver.find_element(By.XPATH, "//span[@class='text error' and @id='fgx-brand-locateDealerMsgError']")
    dealer_names = driver.find_elements(By.CLASS_NAME, "dealer-name")
    distance = driver.find_elements(By.XPATH, "//span[@class='distance']")
    address = driver.find_elements(By.CLASS_NAME, "street-city-state-zip")
    telephone = driver.find_elements(By.XPATH, "//span[@class='text phone-link']")

    print("Dealer found for zip-code:", zip_code)
    # index_id = driver.find_elements(By.CLASS_NAME, "index")

    # Check if the CSV file exists and is empty
    if not os.path.exists('dealer_info.csv') or os.stat('dealer_info.csv').st_size == 0:
        with open('dealer_info.csv', 'w', newline='', encoding='utf-8') as csvfile:
            # Create a CSV writer object
            csv_writer = csv.writer(csvfile)
            # Write the header row
            csv_writer.writerow(['Dealer Name', 'Distance', 'Address', 'Telephone'])

    # Open a CSV file in write mode
    with open('dealer_info.csv', 'a', newline='', encoding='utf-8') as csvfile:
        # Create a CSV writer object
        csv_writer = csv.writer(csvfile)
        # Iterate over the elements and write each row to the CSV file
        for i in range(len(dealer_names)):
            # index = index_id[i].text
            name = dealer_names[i].text
            dist = distance[i].text
            addr = address[i].text
            # Extract telephone numbers
            telephone_numbers = [tel.text.strip() for tel in telephone]
            tel = telephone_numbers[i]
            print(name , dist, addr, tel)
            csv_writer.writerow([name, dist, addr, tel])
    print("Data has been scraped and stored in dealer_info.csv for url:{0} and zip-code:{1}".format(url, zip_code))

# Read zip codes from Excel file
zip_codes_df = pd.read_excel('test.xlsx')
zip_codes = zip_codes_df['zip']
# Iterate through zip codes and scrape data
for zip_code in zip_codes:
    scrape_data(zip_code)