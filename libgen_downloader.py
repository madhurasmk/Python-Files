
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
def download_book(book_name):
    download_folder = r"C:\\Books"  # Use raw string to avoid escape issues
    
    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": download_folder}
    options.add_experimental_option("prefs", prefs)
    
    # Initialize WebDriver
    driver = webdriver.Chrome(options=options)
    
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
    
    # Wait for the download to complete
    while True:
        # time.sleep(1)
        downloaded_files = os.listdir(download_folder)
        if any(file.endswith('.pdf') or file.endswith('.epub') for file in downloaded_files):
            break
    
    # Check if the downloaded file is in the correct format
    valid_files = [file for file in downloaded_files if file.endswith('.pdf') or file.endswith('.epub')]
    
    if valid_files:
        os.startfile(download_folder)
        print("Download completed. The file is saved in the folder: {download_folder}")
    else:
        print("No valid EPUB or PDF file was downloaded.")    
    driver.quit()
if __name__ == "__main__":
    book_name = input("Enter the name of the book to be downloaded: ")
    download_book(book_name)    
