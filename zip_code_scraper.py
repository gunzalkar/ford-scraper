import time
import urllib.request as req
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException  # Add this import
from webdriver_manager.chrome import ChromeDriverManager
import csv

# Setting up the Chrome webdriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

def scrape_data(zip_code):
    # Format zip code to ensure it has leading zeros
    formatted_zip = f'{zip_code:05d}'
    url = f'https://www.ford.com/dealerships/#/q/{formatted_zip}/radius/50'
    driver.get(url)
    
    # Wait for the page to load
    try:
        WebDriverWait(driver, 20).until(ec.presence_of_element_located((By.CLASS_NAME, "dealer-name")))
    except TimeoutException:
        print(f"Timeout occurred while waiting for page to load for zip code {formatted_zip}. Skipping.")
        return
    
    # Check if there is an error message element
    error_message = driver.find_elements(By.ID, "fgx-brand-locateDealerMsgError")
    if error_message:
        print(f"No data available for zip code {formatted_zip}. Moving to the next zip code.")
        return
    
    while True:
        try:
            # Find the "View More Dealers" button by its text content
            view_more_button = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH, "//button[contains(., 'View More Dealers')]")))
            # Click the button
            view_more_button.click()
            time.sleep(2)  # Wait for page to load (you can adjust this time if needed)
        except:
            # If the button is not found, break the loop
            break

    # Once the full page is loaded and the button disappears, scrape the dealer names
    index_id = driver.find_elements(By.CLASS_NAME, "index")
    dealer_names = driver.find_elements(By.CLASS_NAME, "dealer-name")
    distances = driver.find_elements(By.CLASS_NAME, "distance")
    addresses = driver.find_elements(By.CLASS_NAME, "street-city-state-zip.bri-txt.body-two.ff-b")
    telephones = driver.find_elements(By.CLASS_NAME, "telephone")

    # Write data to CSV file
    with open('dealers.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for i in range(len(index_id)):
            writer.writerow([index_id[i].text.strip(),
                             dealer_names[i].text.strip(),
                             distances[i].text.strip(),
                             addresses[i].text.strip(),
                             telephones[i].text.strip(),
                             url])

# Read zip codes from Excel file
zip_codes_df = pd.read_excel('zip_codes.xlsx')
zip_codes = zip_codes_df['zip']

# Write header to CSV file
with open('dealers.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Index', 'Dealer Name', 'Distance', 'Address', 'Telephone', 'URL'])

# Iterate through zip codes and scrape data
for zip_code in zip_codes:
    scrape_data(zip_code)
