import os

def scan_folder(folder_path):
    supported_formats = ('.azw3', '.mobi', '.epub')
    files = [f for f in os.listdir(folder_path) if f.endswith(supported_formats)]
    return files
import requests
from bs4 import BeautifulSoup

def convert_file(file_path, output_folder):
    # Example using an online conversion service
    url = 'https://www.pdf2go.com/result'
    files = {'file': open(file_path, 'rb')}
    response = requests.post(url, files=files)
    
    # Parse the response to get the download link
    soup = BeautifulSoup(response.content, 'html.parser')
    link_tag = soup.find("a", href=lambda x:x and 'download-file' in soup)
    print(link_tag, "link_tag....")
    if link_tag:
        download_link = link_tag['href']
        file_name = link_tag.text.strip()
        
    # download_link = soup.find('a')['data-original-title']
    print("Download link:", download_link)
    # Download the converted file
    download_response = requests.get(download_link, stream=True)
    if response.status_code == 200:
        output_folder = "C:/Books"
        os.makedirs(output_folder, exist_ok=True)
        file_path = os.path.join(output_folder, file_name)
        
    # output_file_path = os.path.join(output_folder, os.path.basename(file_path).replace('.azw3', '.pdf').replace('.mobi', '.pdf').replace('.epub', '.pdf'))
        with open(file_path, 'wb') as output_file:
            output_file.write(download_response.content)
    
    return file_path
def delete_original_file(file_path):
    os.remove(file_path)
def main(folder_path):
    files = scan_folder(folder_path)
    for file in files:
        file_path = os.path.join(folder_path, file)
        try:
            converted_file_path = convert_file(file_path, folder_path)
            # delete_original_file(file_path)
            print(f"Converted and deleted: {file}")
        except Exception as e:
            print(f"Failed to convert {file}: {e}")

if __name__ == "__main__":
    folder_path = 'C:/Books'
    main(folder_path)
