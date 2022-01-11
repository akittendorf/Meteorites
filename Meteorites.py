import pandas as pd

meteors = pd.read_csv('Meteorite_Landings.csv')

# remove the nametype field
meteors.drop(columns=['nametype'], inplace=True)

# clean the mass (g) field so values default to 0
meteors['mass (g)'].fillna(0, inplace=True)

# There is missing year data. Determine whether to handle it. *missing data dropped*
meteors.dropna(axis=0, subset=['year'], inplace=True)

# Format the date in MM/dd/yyyy with the time in hours:minutes:seconds AM/PM
meteors['year'] = meteors['year'].astype(str) # already formatted correctly

# Make sure that when the data is imported that all diacritics (umlauts over o's - for example - as in records 44806, 44843-44847 show) are loaded.

# store each decade's data in its own Excel sheet
meteors['YEAR'] = meteors['year'].apply(lambda x: x[-16:-12]) # create temp YEAR column
meteors['YEAR'] = meteors['YEAR'].astype(int)
decades = []
for decade in range(meteors['YEAR'].min(), 2020, 10):
    data = meteors[(meteors['YEAR'] > decade) & (meteors['YEAR'] < decade+10)]
    decades.append(data)
with pd.ExcelWriter('meteorites_by_decade.xlsx') as xlsxWriter:
    title = meteors['YEAR'].min()
    for df in decades:
        final = df.drop(columns=['YEAR'])
        final.to_excel(xlsxWriter,sheet_name=str(title))
        title+=10