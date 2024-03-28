import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import base64
from io import BytesIO

url = "https://fireemblem.fandom.com/wiki/Category:Lists"

# Send a GET request to the URL
response = requests.get(url)

# Parse the HTML content of the page
soup = BeautifulSoup(response.content, "html.parser")

# Find all <a> tags with class "category-page__member-link"
titles = soup.find_all('a', class_= "category-page__member-link")

# Find all <a> tags with class "category-page__member-link"
titles = soup.find_all('a', class_= "category-page__member-link")

titles = soup.find_all('a', class_="category-page__member-link")
url = url.strip('/Category:Lists')
# Find all <a> tags with class "category-page__member-link"
titles = soup.find_all('a', class_="category-page__member-link")
character_list = []
title_list = []
for title in titles:
    # Extract the title text using the .text attribute
    act_title = title.text.strip()
    # Check if the title contains "List of characters"
    if "List of characters" in act_title:
        # Get the URL associated with the title
        href = title['href']
        # Construct the full URL by appending href to the base URL
        full_url = url + href
        # Send a request to the full URL
        response_inner = requests.get(full_url)
        # Parse the HTML content of the inner page
        soup_inner = BeautifulSoup(response_inner.content, "html.parser")
        # Find all divs with class 'p-container'
        boxes = soup_inner.find_all('div', class_='p-container')
        # Iterate over each div
        for box in boxes:
            # Find the div with class 'link' which contains the character name
            inner_boxes = box.find('div', class_='link')
            # Inside div, find all <a> tags and get the text inside
            characters = inner_boxes.find_all('a')
            # Iterate over each character
            for character in characters:
                character_list.append(character.text.strip())
                title_list.append(act_title.replace("List of characters in Fire Emblem", "").strip())

df = pd.DataFrame({'Character': character_list, 'Title': title_list})
file_path = "characters.xlsx"
df.to_excel(file_path, index=False)
print(df)
# parent with class = 'category-page__members-wrapper
# parent has children items with class =  category-page__member
# then children items has a url that needs to send a request
# then in new request get all items with classs = 'p-container'
# in each p-container get the parent item called link 
# then link has an <a> tag that needs to be appended to df 

# in dataframe format 
# each list of characters be in diffeerent sheetse