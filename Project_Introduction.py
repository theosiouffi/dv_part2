import streamlit as st
import pandas as pd
import altair as alt
from vega_datasets import data

st.set_page_config(
    page_title="World Happiness Data Explorer Project",
    page_icon="🌍",
)

st.title("World Happiness Data Explorer Project 🌐")
st.write("Welcome to the World Happiness Data Explorer Project! This project aims to provide an interactive platform for exploring and analyzing world happiness data. You can visualize and compare happiness data across different countries, years, and variables.")


# Read the Excel file
df = pd.read_excel('./data/Data1.xls')

countries_df = pd.read_excel('./data/Iso.xlsx')
countries_df = countries_df.rename(columns={'English short name': 'Country name'})

df = df.merge(countries_df, on='Country name', how='left')

iso_numeric_codes = {
    'Netherlands': 528,
    'United Kingdom': 826,
    'United Arab Emirates': 784,
    'United States': 840,
    'South Korea': 410,
    'Philippines': 608,
    'Vietnam': 704,
    'Dominican Republic': 214,
    'Moldova': 498,
    'Russia': 643,
    'Bolivia': 68,
    'Venezuela': 862,
    'Congo (Brazzaville)': 178,
    'Laos': 418,
    'Ivory Coast': 384,
    'Turkiye': 792,
    'Iran': 364,
    'Tanzania': 834,
    'Comoros': 174,
    'Congo (Kinshasa)': 180,
    "Niger": 566,
    "Gambia": 270,
    "Angola": 24,
    # Note: Some territories like Kosovo, Taiwan, Hong Kong, and State of Palestine have special considerations.
}

# Update the DataFrame
for country, code in iso_numeric_codes.items():
    df.loc[df['Country name'] == country, 'Numeric'] = code

# Special cases (using common placeholders)
df.loc[df['Country name'] == 'Taiwan Province of China', 'Numeric'] = 158
df.loc[df['Country name'] == 'Hong Kong S.A.R. of China', 'Numeric'] = 344
df.loc[df['Country name'] == 'State of Palestine', 'Numeric'] = 275

# First, ensure the Numeric column can accommodate mixed types
df['Numeric'] = df['Numeric'].astype(object)

# Example to re-fill a specific country if missed; repeat as necessary
df.loc[df['Country name'] == 'Specific Country', 'Numeric'] = 'Specific Code'

# After updates, check for any remaining NaNs in the Numeric column
still_missing = df[df['Numeric'].isna()]
print("Countries still missing ISO numeric codes:", still_missing['Country name'].tolist())

df=df.rename(columns={'English short name': 'Country name'})

# Define score ranges/categories directly within the DataFrame
def score_category(score):
    if score > 6:
        return 'High'
    elif score > 4:
        return 'Medium'
    else:
        return 'Low'

df['Score Category'] = df['Ladder score'].apply(score_category)

# Transform your data to include a 'name' field for tooltips
transformed_df = df.copy()
transformed_df['name'] = transformed_df['Country name']  # Ensure this matches your DataFrame

# Your original DataFrame is named df
# Assuming 'Numeric' is the column with ISO numeric codes

# Categorize 'Ladder score' into bins for easier filtering
# This is an additional step for demonstration purposes
df['Score Category'] = pd.cut(df['Ladder score'], bins=[3, 4, 6, 10],
                              labels=['Low', 'Medium', 'High'], right=False)

# Use the provided TopoJSON from Altair's dataset
source = alt.topo_feature(data.world_110m.url, "countries")

# Background map with a light grey fill for all countries
background = alt.Chart(source).mark_geoshape(
    fill="#a7a7a7", stroke=""
).properties(
    width=800,
    height=400
).project('equirectangular')

# Create a radio button selection for Score Category
radio_buttons = alt.binding_radio(options=['Low', 'Medium', 'High'], name='Score Category ')
selection = alt.selection_single(fields=['Score Category'], bind=radio_buttons, empty='all')

# Adjust the heatmap layer to use the new selection
heatmap = alt.Chart(source).mark_geoshape().encode(
    color='Ladder score:Q',
    tooltip=[
        alt.Tooltip('name:N', title='Country'),
        alt.Tooltip('Ladder score:Q', title='Happiness Score')
    ]
).transform_lookup(
    lookup='id',
    from_=alt.LookupData(transformed_df, 'Numeric', ['name', 'Ladder score', 'Score Category'])
).transform_filter(
    selection
).properties(
    width=800,
    height=400
).project(
    type='equirectangular' # Adjust projection to fit the background
).interactive()

st.subheader("World Happiness Heatmap in 2023")
st.write("This heatmap displays the happiness scores of different countries around the world. You can use the radio buttons to filter the countries based on their happiness score categories. Low scores are less than 4, medium scores are between 4 and 6, and high scores are greater than 6.")

# Combine the background and heatmap with added selection
final_chart = (background + heatmap).add_selection(
    selection
)

# Display the final chart directly
st.altair_chart(final_chart)

