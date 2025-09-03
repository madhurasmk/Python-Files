from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

def download_book(book_name):
    # driver_path = r"C:\\Users\\Sangmesh\\ChromeStandaloneSetup64.exe"  # Update with the correct path
    download_folder = r"C:\\Books"  # Use raw string to avoid escape issues
    
    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": download_folder}
    options.add_experimental_option("prefs", prefs)
    
    # Use Service for WebDriver initialization
    # service = Service(driver_path)
    driver = webdriver.Chrome()
    
    driver.get("http://libgen.is/")
    
    search_box = driver.find_element(By.NAME, "req")
    search_box.send_keys(book_name)
    search_box.send_keys(Keys.RETURN)
    
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//table[@class='c']"))
        )
    except:
        print("The book is not available.")
        driver.quit()
        return
    
    rows = driver.find_elements(By.XPATH, "//table[@class='c']//tr")
    latest_year = 0
    latest_row = None
    
    for row in rows[1:]:  # Skip header row
        try:
            year = int(row.find_elements(By.TAG_NAME, "td")[4].text)
            if year > latest_year:
                latest_year = year
                latest_row = row
        except ValueError:
            continue  # Skip rows where the year is not a valid integer
    
    if latest_row:
        mirror_link = latest_row.find_elements(By.TAG_NAME, "td")[9].find_elements(By.TAG_NAME, "a")[0]
        mirror_link.click()
    else:
        print("The book is not available.")
        driver.quit()
        return
    
    try:
        get_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "GET"))
        )
        get_link.click()
    except:
        print("Failed to find the download link.")
        driver.quit()
        return
    
    # time.sleep(10)  # Wait for download to complete (adjust as necessary)
    
    os.startfile(download_folder)
    driver.quit()

if __name__ == "__main__":
    book_name = input("Enter the name of the book to be downloaded: ")
    download_book(book_name)
    print("Download completed. The file is saved in the folder: C:\\Books")