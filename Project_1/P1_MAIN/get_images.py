import os
import requests
from bs4 import BeautifulSoup
import base64

def download_and_save_image(index, title, image_url):
    if not os.path.exists("images"):
        os.makedirs("images")
    
    file_name = f"{index}_{title.replace(':', '').replace(' ', '_').lower()}.png"
    file_path = os.path.join("images", file_name)
    
    if image_url.startswith('data:image'):
        header, data = image_url.split(',', 1)
        image_data = base64.b64decode(data)
        with open(file_path, "wb") as f:
            f.write(image_data)
    else:
        img_data = requests.get(image_url).content
        with open(file_path, "wb") as f:
            f.write(img_data)

url = "https://fireemblem.fandom.com/wiki/Fire_Emblem_Wiki"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
parent = soup.find("div", class_="carousel games")


urls = []
image_urls = []

# Initialize the index
index = 0

# Iterate through each slide in the parent element
for slide in parent.find_all("div", class_="slide"):
    # Extract title
    title = slide.find("span").text.strip().replace('Fire Emblem:', '').strip('')
    # Extract URL
    url = slide.find("a")["href"]
    urls.append(url)
    print(url)
    # Extract image URL
    img = slide.find("img")
    if img and "data-src" in img.attrs:
        img_src = img["data-src"]
        image_url = img_src.split("?")[0]
        image_urls.append(image_url)
        
        # Increment the index before downloading the image
        index += 1
        
        # Download and save image with index and title as filename
        download_and_save_image(index, title, image_url)
