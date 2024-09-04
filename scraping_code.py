from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time
# Set up the WebDriver using webdriver-manager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
try:
    driver.get("https://www.iplt20.com/stats/2008")
    # Set up WebDriverWait
    wait = WebDriverWait(driver, 10)
    # Wait for the "View All" button to be visible and clickable
    view_all_button = wait.until(EC.visibility_of_element_located((By.XPATH, '//a[contains(text(), "View All")]')))
    driver.execute_script("arguments[0].scrollIntoView(true);", view_all_button)
    driver.execute_script("arguments[0].click();", view_all_button)
    # Wait for additional rows to load
    time.sleep(10)  # Increase if necessary
    # Extract the page source after the data is fully loaded
    page_source = driver.page_source
    # Use BeautifulSoup to parse the page source
    soup = BeautifulSoup(page_source, "lxml")
    # Find the table with the specific class
    table = soup.find("table", class_="st-table statsTable ng-scope archiveseason")
    # Extract headers
    header = table.find_all("th")
    titles = [i.text for i in header]
    # Create a DataFrame with the extracted headers
    df = pd.DataFrame(columns=titles)
    # Extract rows and add them to the DataFrame
    rows = table.find_all("tr")
    for row in rows[1:]:  # Skip the header row
        data = row.find_all("td")
        row_data = [td.text for td in data]
        df.loc[len(df)] = row_data
    #print(df)
    df.to_csv("IPL_player_stats_2008.csv")
finally:
    # Quit the WebDriver
    driver.quit()


