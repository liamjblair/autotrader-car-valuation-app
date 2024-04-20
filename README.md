## AutoTrader Car Valuation App

# Overview: 

This is a simple project I created for fun to help me with selling my car. Web scrapping can be fun, so I wanted to do something useful with it too. Simply follow the prompts and enter your search criteria such as Make, Model, Max Mileage (will give you vehicles up to this value), Postcode (postcode mandatory), variant, ect. Code will output the highest price, lowest and average price found for your car. Which should hopefully assit in giving you an idea how much you should be pricing your car. It will also output all the results to a .csv, useful for further analysis. To avoid too many server requests in a short time, I have added time.sleeps in.

# Installation:
Clone this repository to your local machine.
Install the required Python packages using pip >>
pip install -r requirements.txt

# Usage:
Run the script autotrader_scraper.py.

Follow the prompts to enter the desired search criteria such as make, model, mileage, year, etc.
The script will scrape AutoTrader UK for car listings based on the provided criteria and save the results to a CSV file named AutoTraderTest.csv.
Additionally, it will display some statistics about the scraped data, such as the highest, average, and lowest prices found.

# Dependencies:
Beautiful Soup - For web scraping.
Selenium - For web automation.
Pandas - For data manipulation.
ChromeDriver - https://googlechromelabs.github.io/chrome-for-testing/

# Configuration:
Make sure to have the Chrome WebDriver installed and configured.

# Contributions:
I am always keen to learn better ways of doing things and enjoy seeing how different people approach things! Feel free to submit pull requests or open issues if you encounter any problems!
