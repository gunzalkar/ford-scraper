import time
import csv
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

def scrape_data(url):
    driver.get(url)
    while True:
        try:
            view_more_button = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH, "//button[contains(., 'View More Dealers')]")))
            view_more_button.click()
            time.sleep(2)
        except:
            break

    index_id = driver.find_elements(By.CLASS_NAME, "index")
    dealer_names = driver.find_elements(By.CLASS_NAME, "dealer-name")
    distance = driver.find_elements(By.CLASS_NAME, "distance")
    address = driver.find_elements(By.CLASS_NAME, "street-city-state-zip")
    telephone = driver.find_elements(By.CLASS_NAME, "phone-link")

    # Open a CSV file in write mode
    with open('dealer_info.csv', 'w', newline='', encoding='utf-8') as csvfile:
        # Create a CSV writer object
        csv_writer = csv.writer(csvfile)
        # Write the header row
        csv_writer.writerow(['Index', 'Dealer Name', 'Distance', 'Address', 'Telephone'])
        # Iterate over the elements and write each row to the CSV file
        for i in range(len(index_id)):
            index = index_id[i].text if i < len(index_id) else ''
            name = dealer_names[i].text if i < len(dealer_names) else ''
            dist = distance[i].text if i < len(distance) else ''
            addr = address[i].text if i < len(address) else ''
            tele_element = telephone[i] if i < len(telephone) else None
            try:
                tele = tele_element.find_element(By.CLASS_NAME, "text").text
            except NoSuchElementException:
                tele = ''
            csv_writer.writerow([index, name, dist, addr, tele])

    print("Data has been scraped and stored in dealer_info.csv")

url = 'https://www.ford.com/dealerships/#/q/10012/radius/50'
scrape_data(url)
