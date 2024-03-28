import requests
from bs4 import BeautifulSoup
import pandas as pd

# Define a list to store scraped data
scraped_data = []

# Define a dictionary to map colors to appropriate names
seriesColors = {
    'Red': 'Blade of Light', 
    'Blue': 'Brand', 
    'White': 'Hoshido',
    'Black': 'Nohr',
    'Green': 'Medallion', 
    'Purple': 'Legendary Weapons',
    'Yellow': 'Holy War Flag', 
    'Brown': 'Crest',
    'Colorless': 'Unaffiliated'
}

def scrapeBody(title, href):
    global scraped_data

    response = requests.get(href)

    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all <tbody> tags in the document
        all_tbody_tags = soup.find_all('tbody')

        if len(all_tbody_tags) >= 2:
            cardList = all_tbody_tags[1]
            rows = cardList.find_all('tr')
            for row in rows:
                items = row.find_all('td')
                
                if len(items) >= 4:  
                    card_rarity = items[1].get_text()
                    # adjust the card rarity
                    if 's' in title[-2:] :
                        card_box = title[-1:]
                    else : 
                        card_box = title[-2:]  
                    card_rarity = 'B' + card_box + "-" +  card_rarity[4:]
                    # gets rid of any white space
                    card_rarity = card_rarity.replace(' ', '')
                    # gets rid of any data that , in front
                    card_name = items[2].get_text().lstrip(',')
                    fourth_item = items[3].find('img')
                    # takes sr(+) or any mention of + and adds another row
                    if "+" in card_rarity:
                        alt_text = fourth_item.get('alt') if fourth_item else "Symbolless"
                        card_first_part = card_name.split(":")[0]
                        # Append both rows
                        scraped_data.append([title, card_rarity.replace("+", '').replace("(", '').replace(")", ''), card_name, alt_text, card_first_part])
                        scraped_data.append([title, card_rarity.replace("(", '').replace(")", ''), card_name, alt_text, card_first_part])
                    else:
                    # otherwise just add the card data
                        alt_text = fourth_item.get('alt') if fourth_item else "Symbolless"
                        card_first_part = card_name.split(":")[0]
                        scraped_data.append([title, card_rarity, card_name, alt_text, card_first_part])
                        
    # checks data in the tbody
        else:
            print("Second <tbody> tag not found.")
    else:
        print("Failed to retrieve content from the URL.")
# Define base URL and main page URL
baseURL = "https://wiki.serenesforest.net"
# each box has this url 
mainPage = "https://wiki.serenesforest.net/index.php/Booster_Series"
response = requests.get(mainPage)
# gets request from sernes fortest
if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")
    all_centers = soup.find_all('center')
    # centers will contain paragraphs
    for center in all_centers: 
        paragraphs = center.find_all('p')
        paragraphs.reverse()
    # in paragraphs there are the box card with table data
        for paragraph in paragraphs: 
            links = paragraph.find_all('a', href=True)
            for link in links:

                title = link.get('title')
                href = link.get('href')
                if title:
                    href = baseURL + href
                    # scrapebody goes to each invidual booster box with table data that will be appended to df .
                    print("SCRAPING TITLE:", title)
                    scrapeBody(title, href)
                else:
                    print("No title attribute found.")
else: 
    print("Error: The request was not successful.")

# Create DataFrame using scrapeBody
df = pd.DataFrame(scraped_data, columns=['Title', 'Rarity', 'Name', 'Series Origin', 'Main Name'])

# Define the file path to save the Excel file
file_path = "blank.xlsx"
# df = pd.read_excel(file_path
#                    )
replacement = {
    "Red": "Blade of Light",
    "Blue": "Brand",
    "Purple": "Legendary Weapons",
    "Green": "Medallion",
    "Yellow": "Holy War Flag",
    "Black": "Nohr",
    "White": "Hoshido",
    "Symbolless": "Other",
    "Holy Flag War": "Holy War Flag",
    "Fódlan": "Crest",
    "Yelllow" : "Holy War Flag", 
    "Crests of the Goddess": "Crest",
    "Crest of the Goddess": "Crest",
    "Colorless": "Other"
}
df["Series Origin"] = df["Series Origin"].replace(replacement)
# then count many times card shows up 
df['Name'] = df['Name'].str.replace(r'^([^a-zA-Z?]+)', '').replace(',', '')
# Remove the comma at the beginning of the string
df['Name'] = df['Name'].str.split(',').str[-1]

# Save the DataFrame to the specified file path
name_counts = df['Main Name'].value_counts()
df['Unique Variants'] = df['Main Name'].map(name_counts)

rares =df['Rarity']
titles = df['Title']
# cleaning the rarity and titles 
for index, row in df.iterrows():
    rare = row['Rarity']
    title = row['Title']

    
    # Extracting the first and second digits from rarity
    F = rare[1]
    L = rare[2]

    # Checking if F is '0' to decide title
    if F == '0':
        title = "Booster Series" + " " +L
    else:
        title = "Booster Series" + " " +  F + L
    



    # Assigning the updated title back to the row
    df.at[index, 'Title'] = title

df.to_excel(file_path, index=False)
print("Data saved to", file_path)
