import pandas as pd

# Read the data from the files
scrape_data = 'pandas_data.xlsx'
s_df = pd.read_excel(scrape_data)
cipher_cards = set(s_df['Main Name'])  # Convert to set for faster lookup

final_data = 'characters.xlsx'
df = pd.read_excel(final_data)

# need to add (Male) or (Female)
# Create a new column 'In Cipher' and initialize it with False
df['In Cipher'] = False

# Compare characters and mark if they are in 'cipher_cards' or variants
for index, character in enumerate(df['Character']):
    if character in cipher_cards:
        df.at[index, 'In Cipher'] = True
    elif f"{character} (Male)" in cipher_cards or f"{character} (Female)" in cipher_cards:
        df.at[index, 'In Cipher'] = True
    elif f"{character} (Fódlan)" in cipher_cards:
        df.at[index, 'In Cipher'] = True
    elif f"{character} (Judgral)" in cipher_cards:
        df.at[index, 'In Cipher'] = True

# Save the modified DataFrame back to the Excel file
df.to_excel(final_data, index=False)
