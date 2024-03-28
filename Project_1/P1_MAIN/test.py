import pandas as pd

# Read the data from the Excel file
scraped = 'pandas_data.xlsx'
df = pd.read_excel(scraped)
main_names =df[['Main Name', ]].unique()

# compare to scrape with wiki
wiki = 'characters.xlsx'
characters = df['Character'].unique()
df_c = pd.read_excel(wiki)



