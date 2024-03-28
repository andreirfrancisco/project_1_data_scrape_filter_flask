from flask import Flask, render_template, request
import pandas as pd
import os
import re
from collections import Counter


app = Flask(__name__)
characters_path = 'characters.xlsx'
df_c = pd.read_excel(characters_path)
file_path = "pandas_data.xlsx"
df = pd.read_excel(file_path)
characters = df['Main Name']
image_folder = "images"  # Path to the folder named "images"
image_names = os.listdir(image_folder)
image_names.sort(key=lambda x: int(x.split('_')[0]))  # Sorting image names
# Load character data from Excel file
characters_path = 'characters.xlsx'
df_c = pd.read_excel(characters_path)
titles = df_c['Title'].unique()

def create_img(data):
    # Filter the DataFrame based on the provided main name
    rares = df[df['Main Name'] == data]
    
    # Initialize lists to store x and y data
    x_data = []
    
    # Iterate through rarities and extract different rarity categories
    for rare in rares['Rarity']:
        # Use regular expression to remove any numerical values from the rarity label
        rarity_category = re.sub(r'\d', '', str(rare).replace('B', '').replace('-', ''))
        # Exclude rarity categories like "B-"
        if rarity_category != 'B-':
            # Append the rarity category to the list
            x_data.append(rarity_category)
    
    # Count the frequency of each rarity category
    rarity_counts = pd.Series(x_data).value_counts()
    
    # Extract rarity categories and their counts
    x_data = rarity_counts.index.tolist()  # rarity categories
    y_data = rarity_counts.values.tolist()  # counts
    
    return x_data, y_data

@app.route('/')
def index():
    series = sorted(df['Cipher Category'].unique())
    search_options = sorted(characters.unique())
    return render_template('index.html', titles=series, search_options=search_options, image_names=image_names)

@app.route('/image_detail', methods=['GET'])
def image_detail():
    image_name = request.args.get('image_name')
    print("Image Name:", image_name)  # Print image_name for debugging
    # count of all total rares
    total_cards =[]
    wanted_characters = []

    for file in image_names:
        if image_name in file:
            print("WANTED IN:", file)
            for title in titles:
                if title.lower() in file.replace('_', ' ').replace('__', ' '): 
                    print(df_c[df_c['Title'].str.lower() == title.lower()])
                    wanted_characters.append(title)
                    break  # Break out of the loop if a title is found
                else:
                    print(title.lower(), 'w/no match', file.lower())
        else:
            print("NO Match:", file, 'and request', image_name)

    print("Wanted Characters:", wanted_characters)

    yes_ciphers = df_c[df_c['Title'].isin(wanted_characters) & (df_c['In Cipher'] == True)]
    yes_ciphers = yes_ciphers.sort_values(by='Character')
    no_ciphers = df_c[df_c['Title'].isin(wanted_characters) & ~df_c['In Cipher']]
    no_ciphers = no_ciphers.sort_values(by ='Character')
    print("IN", yes_ciphers)
    print("NOT", no_ciphers)
    return render_template('series.html', image_name=image_name, 
                           yes_ciphers=yes_ciphers['Character'], no_ciphers=no_ciphers['Character']
                           , image_names = image_names, 
                           total_cards = total_cards)

@app.route('/search', methods=['GET'])
def search():
    search_term = request.args.get('term', '').strip().capitalize()
    filtered_rows = df[df['Main Name'].str.capitalize() == search_term]

    if not filtered_rows.empty:
        character = filtered_rows.iloc[0]  # Assuming you want to take the first character if there are multiple matches
        print("Character:", character)  # Print the character for debugging
        data = create_img(search_term)
        rare_w_c = df[['Main Name', 'Rarity']]
        clean = rare_w_c[['Main Name', 'Rarity']]
        variations = []
        different_rares =[]
        for index, row in clean.iterrows():
            if search_term.lower() in row['Main Name'].lower():
                variations.append(row['Rarity'])
                different_rares.append(re.sub(r'\d', '', row['Rarity'][-4:]))

        # Count unique rarity values
        rarity_counter = Counter(different_rares)
        # Extract x_data and y_data for Chart.js
        x_data = list(rarity_counter.keys())
        y_data = list(rarity_counter.values())

        return render_template('character.html', search_term=search_term,
                                variations=variations, 
                                card_origin=character['Cipher Category'], 
                                image_names=image_names, 
                                rarity_data=data, 
                                different_rares=different_rares,
                                x_data=x_data,
                                y_data=y_data)
    else:
        # Handle the case when no matching character is found
        return render_template('not_found.html', search_term=search_term, image_names = image_names)


if __name__ == '__main__':
    app.run(debug=True)
