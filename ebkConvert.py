import os
import requests
from bs4 import BeautifulSoup

import time

def convert_file(file_path, output_folder):
    url = 'https://cloudconvert.com/epub-to-pdf'
    with open(file_path, 'rb') as file:
        files = {'file': file}
        response = requests.post(url, files=files)
    
    # Check if the upload was successful
    if response.status_code != 200:
        print(f"Error: Failed to upload file {file_path}")
        return None
    
    # Parse the response to find the conversion status page
    soup = BeautifulSoup(response.content, 'html.parser')
    status_page_tag = soup.find('a') ['href']
    
    if not status_page_tag:
        print("Error: Status page link not found!")
        print("Response content:", response.text[:500])  # Print part of the response for debugging
        return None
    
    status_page_link = status_page_tag['href']
    
    # Wait for the conversion to complete
    time.sleep(10)  # Adjust the sleep time as needed
    
    # Check the status page for the download link
    status_response = requests.get(status_page_link)
    status_soup = BeautifulSoup(status_response.content, 'html.parser')
    download_tag = status_soup.find('a', {'download': 'href'})
    
    if not download_tag:
        print("Error: Download link not found!")
        print("Response content:", status_response.text[:500])  # Print part of the response for debugging
        return None
    
    download_link = download_tag['href']
    download_response = requests.get(download_link)
    
    output_file_path = os.path.join(output_folder, os.path.basename(file_path).replace('.azw3', '.pdf').replace('.mobi', '.pdf').replace('.epub', '.pdf'))
    with open(output_file_path, 'wb') as output_file:
        output_file.write(download_response.content)
    
    return output_file_path

def scan_folder(folder_path):
    supported_formats = ('.azw3', '.mobi', '.epub')
    files = [f for f in os.listdir(folder_path) if f.endswith(supported_formats)]
    return files

def delete_original_file(file_path):
    os.remove(file_path)

def main(folder_path):
    files = scan_folder(folder_path)
    for file in files:
        file_path = os.path.join(folder_path, file)
        try:
            converted_file_path = convert_file(file_path, folder_path)
            if converted_file_path:
                delete_original_file(file_path)
                print(f"Converted and deleted: {file}")
            else:
                print(f"Conversion failed for: {file}")
        except Exception as e:
            print(f"Failed to convert {file}: {e}")

if __name__ == "__main__":
    folder_path = 'C:\\Books'  # Change this to your folder path
    main(folder_path)


