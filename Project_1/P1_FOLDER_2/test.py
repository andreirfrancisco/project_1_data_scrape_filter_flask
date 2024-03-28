import pandas as pd

# Define file path and read the Excel files
file = 'blank.xlsx'
new = 'test(2).xlsx'

df = pd.read_excel(file)

rares = df['Rarity']  # Selecting the 'Rarity' column
titles = df['Title']

compare = []
modified_rows = []  # Store modified rows to add to new DataFrame

for index, rare in rares.items():
    # then we do this for the rarity 
    compare.append(rare[1:3])
    print(compare)  # Debugging: Print compare to check its content
    if len(compare) == 3:
        # Check if the second element is different from the other two
        if compare[1] != compare[0] or compare[1] != compare[2]:  
            # Construct new_rare based on the second element of compare and the previous row's 'Rarity'
            new_rare = "B" + compare[1] + df.at[index - 1, 'Rarity'][4:]
            modified_rows.append(new_rare)
        compare.clear()
    else : 
        modified_rows.append(rare[1:3])
# Convert modified_rows list to a DataFrame
new_df = pd.DataFrame(modified_rows, columns=['Rarity'])

# Save the new DataFrame to the existing Excel file specified by 'new'
new_df.to_excel(new, index=False)  # Save to Excel file without index
