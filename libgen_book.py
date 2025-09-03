def get_book_name():
    book_name = input("Enter the name of the book to be downloaded: ")
    return book_name

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def search_book(book_name):
    download_folder = "C:/Books"
    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": download_folder}
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=options)  # Ensure ChromeDriver is in your PATH or provide the path to it
    driver.get('http://libgen.is/')

    search_box = driver.find_element(By.NAME, 'req')
    search_box.send_keys(book_name)
    search_box.send_keys(Keys.RETURN)

    time.sleep(5)  # Wait for the search results to load

    return driver, download_folder

def terminate_driver(driver):
    try:
        driver.quit()
    except Exception as e:
        print(f"Error terminating the driver: {e}")
def handle_search_results(driver):
    try:
        results_table = driver.find_element(By.XPATH, '//table[@class="c"]')
        rows = results_table.find_elements(By.TAG_NAME, 'tr')[1:]  # Skip the header row

        if not rows:
            print("No results found for the book.")
            driver.quit()
            return None

        latest_year = 0
        latest_row = None

        for row in rows:
            columns = row.find_elements(By.TAG_NAME, 'td')
            year_text = columns[4].text.strip()  # Get the text in the year column
            
            if year_text:  # Only proceed if the year text is not empty
                try:
                    year = int(year_text)
                except ValueError:
                    # Handle cases where the year cannot be converted to an integer
                    print(f"Skipping row due to invalid year: {year_text}")
                    continue
            else:
                # If the year text is empty, skip the row
                print("Skipping row with empty year.")
                continue

            if year > latest_year:
                latest_year = year
                latest_row = row

        if latest_row:
            # Wait for the mirror link to be clickable
            mirror_link = WebDriverWait(latest_row, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, '[1]'))
            )
            mirror_link.click()

            # Wait for the next page to load and the "GET" link to be clickable
            get_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, 'GET'))
            )
            get_link.click()

            time.sleep(5)  # Wait for the download to start

            print("Download started.")
            return True

    except Exception as e:
        print(f"An error occurred: {e}")
        terminate_driver(driver)
        return None

def main():
    book_name = get_book_name()
    driver, download_folder = search_book(book_name)
    if driver:
        handle_search_results(driver)
        print(f"Download completed. The file is saved in the folder: {download_folder}")

if __name__ == "__main__":
    main()
