import requests
from bs4 import BeautifulSoup

url = "https://fireemblem.fandom.com/wiki/List_of_characters_in_Fire_Emblem:_Three_Houses"

# Send a GET request to the URL
response = requests.get(url)

div_class="category-page__members-wrapper"
# string has  >>> 
find_string = "List Of characters in Fire Emblem:"
# find all <a> tag with href
a_tag = ['category-page__member-link', 'href']
<a href="/wiki/List_of_characters_in_Fire_Emblem_Awakening" class="category-page__member-link" title="List of characters in Fire Emblem Awakening">List of characters in Fire Emblem Awakening</a>
# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, 'html.parser')
    games = soup.find_all()
    # Find all div elements with class 'link'
    link_divs = soup.find_all('div', class_='link')

    # Loop through each div with class 'link'
    for div in link_divs:
        # Find all <a> tags within this div
        link_tags = div.find_all('a')
        
        # Loop through each <a> tag
        for a_tag in link_tags:
            # Extract the title attribute
            title = a_tag.get('title')
            
            # Print the title
            print("Title:", title)
else:
    print("Failed to retrieve the webpage")
