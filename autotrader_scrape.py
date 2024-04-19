
import os
import sys
from bs4 import BeautifulSoup
import pandas as pd
import math
from urllib.request import urlopen as url_req
import time
import requests
from selenium import webdriver  
from selenium.webdriver.chrome.options import Options
import constants


def make_soup(url):
    driver = webdriver.Chrome(constants.CHROME_DRIVER)
    driver.get(url)
    time.sleep(10) 
    source = driver.page_source
    results = BeautifulSoup(source, "html.parser")

    return results  


def build_url(**kwargs):
    base_url = 'https://www.autotrader.co.uk/car-search?sort=relevance'

    url_parms = ""
    for key, parm in kwargs.items():

        if parm != "":
            if key == "mileage":
                url_parms += f"&maximum-{key}=" + str(parm)
            elif key == "fueltype":
                url_parms += f"&fuel-type=" + str(parm)
            elif key == "year":
                url_parms += f"&{key}-from=" + str(parm)
                url_parms += f"&{key}-to=" + str(parm)
            elif key == "variant":
                url_parms += "&aggregatedTrim=" + str(parm)
            elif key == "transmission":
                url_parms += f"&{key}=" + str(parm)
            else:
                url_parms += f"&{key}=" + str(parm)
   
    return base_url + url_parms

# TODO validate user inputs
make = input("Enter make (eg Ford, BMW): ")
model = input("Input model: ")
mileage = input("Enter max mileage: ")
variant = input("Enter variant: ").title()
year = input("Enter year: ")
postcode = input("Enter postcode: ")
if postcode == "":
    print("Postcode required. Please enter a postcode >> ")
    postcode = input("Enter postcode: ")
    if postcode == "":
        print("Postcode not entered. Exiting program...")
        sys.exit()
distance = input("Enter distance: ")
fuelType = input("Enter fueltype: ").title()
transmission = input("Enter transmission: ").title()

# add %20 for any spaces in the make name (required for valid url)
make = make.replace(" ", "%20") 
model = model.replace(" ", "%20")

url = build_url(make=make,
                model=model,
                mileage=mileage,
                year=year,
                postcode=postcode,
                distance=distance,
                fuelType=fuelType,
                variant=variant,
                transmission=transmission
                )
# TODO log url etc to logging
soup = make_soup(url)

cars_found = soup.find('h1', class_= "at__sc-1n64n0d-5 at__sc-1ldcqnd-4 ldLGbL iKpNlQ")
cars_found = cars_found.text

pages_found = soup.find("p", class_="at__sc-1n64n0d-9 kybQww").text
num_of_pages = int(pages_found.split()[-1])

print(f"Found {cars_found} cars matching this criteria. {num_of_pages} pages found.")

file = "AutoTraderTest.csv"
f = open(file, 'w')
headers = 'price, year, mileage, engine_size, power, transmission, fueltype, page_num, url\n'
f.write(headers)
num_of_cars = 0
for page in range(num_of_pages):
    
    new_url = url + '&page=' + str(page + 1)
    print(f"Page URL - {new_url}")
    page_results = make_soup(new_url)
    
    cars = page_results.find_all("section", attrs={"data-testid": "trader-seller-listing"})
    
    for car in cars:
        num_of_cars += 1
        try:
            price = car.find('span', class_='at__sc-1mc7cl3-5 edXwbj')
            price = price.text
            price = str(price).replace("£", "").replace(",", "")

            raw_specs = car.find("ul", class_="at__sc-1mc7cl3-7 kuBkId")

            specs = [li.get_text(strip=True) for li in raw_specs.find_all('li')]
            year = specs[0]
            mileage = specs[2]
            mileage = str(mileage).replace(",","").replace(" miles", "")
            engine_size = specs[3]
            power = specs[4]
            transmission = specs[5]
            fueltype = specs[6]

            f.write(f"{price}, {year}, {mileage}, {engine_size}, {power}, {transmission}, {fueltype}, {page}, {new_url}\n")

        except Exception as e:
            print(str(e))

print(f"Number of cars iterated over {num_of_cars}")
f.close()        

results = pd.read_csv(file)
max_price = results.price.max()
avg_price = round(results.price.mean(), 2)
min_price = results.price.min()
prices = f"""

        Highest price found: {max_price}\n
        Avgerage price: {avg_price}\n
        Lowest price found: {min_price}

    """

print(prices)
