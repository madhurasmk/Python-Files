from bs4 import BeautifulSoup
import requests
import os
class Website:
    url: str
    title: str
    text: str
    def __init__(self, url):
        self.url = url

        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.title = soup.title.string if soup.title else "No title found"
        for irrelev in soup.body(['script', 'style', 'input']):
            irrelev.decompose()
        self.text = soup.body.get_text(separator="\n", strip=True)

# ed = Website("https://www.hudsonlibrary.org/")
# print(ed.title)
# print(ed.text)

url1 = "https://www.hudsonlibrary.org/"
response = requests.get(url1)
soup1 = BeautifulSoup(response.content, 'html.parser')
for irrelev in soup1.body(['script', 'style', 'input']):
    irrelev.decompose()
text = soup1.body.get_text(separator="\n", strip=True)
print(text)

