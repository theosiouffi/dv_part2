import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Deep Dive by Country", page_icon="🌍")

st.title("Country-Level Comparison of World Happiness Data")
st.write(
    """In this section, you can select multiple countries and compare their variables over time. Here, 
    we also provide a correlation matrix for each selected country.
    """
)

# Load and preprocess data
df1 = pd.read_csv("/Users/theosiouffi/Downloads/dv_part2/happiness_data.csv")
df2 = pd.read_csv("/Users/theosiouffi/Downloads/dv_part2/2023_happy_data.csv")

df1.drop(["Positive affect", "Negative affect", "Life Ladder"], axis=1, inplace=True)
df1.rename(columns={'Healthy life expectancy at birth': 'Healthy life expectancy', 'Log GDP per capita': 'GDP per capita'}, inplace=True)

df2 = df2.iloc[:, :-8]
df2.drop(["Standard error of ladder score", "upperwhisker", "lowerwhisker", "Ladder score"], axis=1, inplace=True)
df2.rename(columns={'Logged GDP per capita': 'GDP per capita'}, inplace=True)
df2['year'] = 2023

df = pd.concat([df1, df2])
df = df.sort_values(by=['Country name', 'year'])
df = df.reset_index(drop=True)

# Country selection - allow multiple selections
country_list = df['Country name'].unique()
selected_countries = st.sidebar.multiselect('Select Countries', country_list, default=country_list[:3])  # Default to the first 3 countries

# Year range filter for line graph
year_range = st.slider("Select year range", min_value=df['year'].min(), max_value=df['year'].max(), value=(df['year'].min(), df['year'].max()))

# Filter data based on selected countries
df_filtered = df[df['Country name'].isin(selected_countries) & df['year'].between(year_range[0], year_range[1])]

    # Visualizations: Line graph
st.subheader("Compare Different Country Variables Over Time")
variable = st.selectbox("Select variable", df.columns[2:])  # Exclude 'Country name' and 'year'
if variable and selected_countries:
    chart = alt.Chart(df_filtered).mark_line().encode(
        x='year',
        y=alt.Y(variable, title=variable),
        color='Country name'
    ).properties(
        width=600,
        height=400
    )
    st.altair_chart(chart)

# Create a container to hold all the charts
st.subheader("Correlation Matrix for Selected Countries")
st.write("This section displays the correlation matrix for the selected countries. The correlation matrix shows the relationship between different variables in the data. Each time a country is selected, a new correlation matrix is generated, allowing you to compare the relationships between variables for different countries.")

charts_container = st.container()

for country in selected_countries:
    # Filter data based on selected country
    df_country = df[df['Country name'] == country]

    # Compute correlation matrix for the selected country
    corr = df_country.drop(['Country name', 'year'], axis=1).corr()

    # Convert correlation matrix to long format for Altair
    corr_df = corr.reset_index().melt('index').rename(columns={'index': 'Variable 1', 'variable': 'Variable 2', 'value': 'Correlation'})
    corr_chart = alt.Chart(corr_df).mark_rect().encode(
        x=alt.X('Variable 1:N', sort='-y'),
        y=alt.Y('Variable 2:N'),
        color='Correlation:Q',
        tooltip=['Variable 1', 'Variable 2', 'Correlation']
    ).properties(
        title=f'Correlation Matrix for {country}',
        width=300,
        height=500
    ).configure_axis(
        labelFontSize=10,
        titleFontSize=12
    )

    # Display the chart in the container
    charts_container.altair_chart(corr_chart, use_container_width=True)

