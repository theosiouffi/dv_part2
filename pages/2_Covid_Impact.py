import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt

st.set_page_config(page_title="Covid Impact Analysis", page_icon="🦠")


# Replace with this when everything is in same folder
#precovid = pd.read_excel('Data 2017-2019.xls')
#covid = pd.read_excel('Data 2020-2022.xls')


# Using this one while using streamlit locally
precovid = pd.read_excel('data/Data 2017-2019.xls')
covid = pd.read_excel('data/Data 2020-2022.xls')

### Format data

# Drop unexpected columns
covid = covid.drop(['Unnamed: 19','Unnamed: 20','Unnamed: 21'], axis=1)

# Filtering precovid to mantain only data that is available in both files
countries = [country for country in precovid['Country name'] if country in covid['Country name'].tolist()]

# Filter both df
precovid = precovid[precovid['Country name'].isin(countries)]
covid = covid[covid['Country name'].isin(countries)]

columns = ['Country name',
 'Ladder score',
'Explained by: Log GDP per capita',
 'Explained by: Social support',
 'Explained by: Healthy life expectancy',
 'Explained by: Freedom to make life choices',
 'Explained by: Generosity',
 'Explained by: Perceptions of corruption',
 'Dystopia + residual']

precovid = precovid[columns]
covid = covid[columns]

## Calculating Difference

# Merging df
difference = precovid.merge(covid, on = 'Country name', suffixes=('_precovid', '_covid'))
# Getting difference in score
difference['Ladder score difference'] = difference['Ladder score_covid'] - difference['Ladder score_precovid']
# Dictionary to map country to continent
country_to_continent = {
    'Finland': 'Europe', 'Denmark': 'Europe', 'Switzerland': 'Europe', 'Iceland': 'Europe', 'Norway': 'Europe',
    'Netherlands': 'Europe', 'Sweden': 'Europe', 'New Zealand': 'Oceania', 'Austria': 'Europe', 'Luxembourg': 'Europe',
    'Canada': 'North America', 'Australia': 'Oceania', 'United Kingdom': 'Europe', 'Israel': 'Asia', 'Costa Rica': 'North America',
    'Ireland': 'Europe', 'Germany': 'Europe', 'United States': 'North America', 'Belgium': 'Europe', 'United Arab Emirates': 'Asia',
    'Malta': 'Europe', 'France': 'Europe', 'Mexico': 'North America', 'Taiwan Province of China': 'Asia', 'Uruguay': 'South America',
    'Saudi Arabia': 'Asia', 'Spain': 'Europe', 'Guatemala': 'North America', 'Italy': 'Europe', 'Singapore': 'Asia',
    'Brazil': 'South America', 'Slovenia': 'Europe', 'El Salvador': 'North America', 'Kosovo': 'Europe', 'Panama': 'North America',
    'Slovakia': 'Europe', 'Uzbekistan': 'Asia', 'Chile': 'South America', 'Bahrain': 'Asia', 'Lithuania': 'Europe',
    'Poland': 'Europe', 'Colombia': 'South America', 'Cyprus': 'Europe', 'Nicaragua': 'North America', 'Romania': 'Europe',
    'Mauritius': 'Africa', 'Kazakhstan': 'Asia', 'Estonia': 'Europe', 'Philippines': 'Asia', 'Hungary': 'Europe',
    'Thailand': 'Asia', 'Argentina': 'South America', 'Honduras': 'North America', 'Latvia': 'Europe', 'Ecuador': 'South America',
    'Portugal': 'Europe', 'Jamaica': 'North America', 'South Korea': 'Asia', 'Japan': 'Asia', 'Peru': 'South America',
    'Serbia': 'Europe', 'Bolivia': 'South America', 'Pakistan': 'Asia', 'Paraguay': 'South America', 'Dominican Republic': 'North America',
    'Bosnia and Herzegovina': 'Europe', 'Moldova': 'Europe', 'Tajikistan': 'Asia', 'Montenegro': 'Europe', 'Russia': 'Europe',
    'Kyrgyzstan': 'Asia', 'Greece': 'Europe', 'Hong Kong S.A.R. of China': 'Asia', 'Croatia': 'Europe', 'Mongolia': 'Asia',
    'Malaysia': 'Asia', 'Vietnam': 'Asia', 'Indonesia': 'Asia', 'Ivory Coast': 'Africa', 'Benin': 'Africa', 'Congo (Brazzaville)': 'Africa',
    'Ghana': 'Africa', 'Nepal': 'Asia', 'China': 'Asia', 'Bulgaria': 'Europe', 'Morocco': 'Africa', 'Cameroon': 'Africa',
    'Venezuela': 'South America', 'Algeria': 'Africa', 'Senegal': 'Africa', 'Guinea': 'Africa', 'Niger': 'Africa', 'Laos': 'Asia',
    'Albania': 'Europe', 'Cambodia': 'Asia', 'Bangladesh': 'Asia', 'Gabon': 'Africa', 'South Africa': 'Africa', 'Iraq': 'Asia',
    'Lebanon': 'Asia', 'Burkina Faso': 'Africa', 'Gambia': 'Africa', 'Mali': 'Africa', 'Nigeria': 'Africa', 'Armenia': 'Asia',
    'Georgia': 'Asia', 'Iran': 'Asia', 'Jordan': 'Asia', 'Mozambique': 'Africa', 'Kenya': 'Africa', 'Namibia': 'Africa', 'Ukraine': 'Europe',
    'Liberia': 'Africa', 'Uganda': 'Africa', 'Chad': 'Africa', 'Tunisia': 'Africa', 'Mauritania': 'Africa', 'Sri Lanka': 'Asia',
    'Congo (Kinshasa)': 'Africa', 'Myanmar': 'Asia', 'Comoros': 'Africa', 'Togo': 'Africa', 'Ethiopia': 'Africa', 'Madagascar': 'Africa',
    'Egypt': 'Africa', 'Sierra Leone': 'Africa', 'Zambia': 'Africa', 'India': 'Asia', 'Malawi': 'Africa', 'Botswana': 'Africa',
    'Tanzania': 'Africa', 'Zimbabwe': 'Africa', 'Afghanistan': 'Asia'
}

# Mapping country to continent
difference['Continent'] = difference['Country name'].map(country_to_continent)
difference_country = difference.sort_values('Ladder score difference', ascending = True)
difference_country['Percentage diff ladder score'] = (difference_country['Ladder score difference']/difference_country['Ladder score_precovid'])*100
difference_continent = difference.groupby('Continent').agg(
    {'Ladder score_precovid':'mean',
    'Ladder score_covid':'mean',
    'Ladder score difference':'mean',
     'Explained by: Log GDP per capita_precovid':'mean',
     'Explained by: Log GDP per capita_covid':'mean',
     'Explained by: Social support_precovid':'mean',
     'Explained by: Social support_covid':'mean',
     'Explained by: Healthy life expectancy_precovid':'mean',
     'Explained by: Healthy life expectancy_covid':'mean',
     'Explained by: Freedom to make life choices_precovid':'mean',
     'Explained by: Freedom to make life choices_covid':'mean',
     'Explained by: Generosity_precovid':'mean',
     'Explained by: Generosity_covid':'mean',
     'Explained by: Perceptions of corruption_precovid':'mean',
     'Explained by: Perceptions of corruption_covid':'mean',
    }
).reset_index()

difference_continent['Dystopia + residual_precovid'] = difference_continent['Ladder score_precovid'] - (difference_continent['Explained by: Log GDP per capita_precovid'] + difference_continent['Explained by: Social support_precovid'] + difference_continent['Explained by: Healthy life expectancy_precovid'] + difference_continent['Explained by: Freedom to make life choices_precovid'] + difference_continent['Explained by: Generosity_precovid'] + difference_continent['Explained by: Perceptions of corruption_precovid'])
difference_continent['Dystopia + residual_covid'] = difference_continent['Ladder score_covid'] - (difference_continent['Explained by: Log GDP per capita_covid'] + difference_continent['Explained by: Social support_covid'] + difference_continent['Explained by: Healthy life expectancy_covid'] + difference_continent['Explained by: Freedom to make life choices_covid'] + difference_continent['Explained by: Generosity_covid'] + difference_continent['Explained by: Perceptions of corruption_covid'])

difference_continent = difference_continent.sort_values('Ladder score difference', ascending = True)
difference_continent['Percentage diff ladder score'] = (difference_continent['Ladder score difference']/difference_continent['Ladder score_precovid'])*100

# Calculate the difference
change_df = covid.set_index('Country name').subtract(precovid.set_index('Country name'))

# Add the 'Period' column with the value 'Change'
change_df['Period'] = 'Change'
change_df = change_df.reset_index()

# Add period to each df
precovid['Period'] = 'PreCovid'
covid['Period'] = 'Covid'
# Concatenate one column into each other
full_period = pd.concat([precovid, covid, change_df], ignore_index = True)
full_period = full_period.sort_values(by = ['Country name','Period'], ascending = [True, False])

new_column_names = {
    'Explained by: Log GDP per capita': 'Log GDP per capita',
    'Explained by: Social support': 'Social support',
    'Explained by: Healthy life expectancy': 'Healthy life expectancy',
    'Explained by: Freedom to make life choices': 'Freedom to make life choices',
    'Explained by: Generosity': 'Generosity',
    'Explained by: Perceptions of corruption': 'Perceptions of corruption'
}

full_period = full_period.rename(columns=new_column_names)


# Moving columns to rows
melted_df = full_period.melt(id_vars=['Country name', 'Ladder score', 'Period'],
                             value_vars=['Log GDP per capita', 'Social support', 'Healthy life expectancy',
                                         'Freedom to make life choices', 'Generosity', 'Perceptions of corruption',
                                         'Dystopia + residual'],
                             var_name='Explained by', value_name='Value')
melted_df = melted_df.sort_values(by = ['Country name', 'Period'], ascending = [True, False]).reset_index(drop=True)
melted_df = melted_df.drop('Ladder score', axis = 1)

#### Plot Starts Here

st.title("Covid Impact over happiness score")
st.write(
    """In this section, we explored how the happiness score changed during covid at country level. 
    You can filter by continent and select the country of your choice by clicking on it. Then you can analyze the overall evolution of happiness score 
    and how each contributor changed during this period for the specific country.  
    """
)

# Define the selection
selection = alt.selection_single(fields=['Country name'], on='click', empty='none', init={'Country name': 'Malta'})

## Continent Filter
continent_dropdown = alt.binding_select(options=difference_country['Continent'].unique().tolist())
continent_selection = alt.selection_single(fields=['Continent'], bind=continent_dropdown, name="Select Continent",init={'Continent': 'Europe'})

# Attempt to directly use the selection in the color encoding
percentage_change = alt.Chart(difference_country).mark_bar().encode(
    x=alt.X('Country name:N', sort='y', axis=alt.Axis(title=None)),
    y=alt.Y('Percentage diff ladder score:Q', axis = alt.Axis(title=None)),
    color=alt.condition(
        selection,
        alt.Color('Percentage diff ladder score:Q', scale=alt.Scale(domain=[0, max(difference_country['Percentage diff ladder score']), min(difference_country['Percentage diff ladder score'])], range=['red', 'green'])),
        alt.value('lightgray')
    ),
    tooltip=['Country name:N', 'Percentage diff ladder score:Q', 'Continent:N']
).add_selection(
    selection
).transform_filter(
    continent_selection
).properties(
    title='Percentage Change in Happiness Score during Covid'
).add_selection(
    continent_selection
)

#st.altair_chart(percentage_change, use_container_width=True)


## Data left plot
left_plot_data = melted_df[melted_df['Period'].isin(['PreCovid', 'Covid'])]

# Lollipop chart for the sum of values
lollipop_chart = alt.Chart(left_plot_data).transform_filter(selection).transform_aggregate(
        total_value='sum(Value)',
        groupby=['Period']
    ).mark_point().encode(
        x=alt.X('Period:N', sort=['PreCovid', 'Covid'], axis=alt.Axis(title=None)),
        y=alt.Y('total_value:Q', axis=alt.Axis(title='Happiness Score')),
        color='Period:N',
        tooltip=['Period:N', 'total_value:Q']
    ).properties(
        title='Score Evolution',
        width=150
    ) + alt.Chart(left_plot_data).transform_filter(selection).transform_aggregate(
        total_value='sum(Value)',
        groupby=['Period']
    ).mark_line().encode(
        x=alt.X('Period:N', sort=['PreCovid', 'Covid'], axis=alt.Axis(title=None)),
        y='total_value:Q'
    )


# Now, for the change between Covid and Not Covid for each "Explained by" factor
# We need to filter for the 'Change' period
change_data = melted_df[melted_df['Period'] == 'Change']

# Visualization for the change in each "Explained by" factor between Covid and Not Covid
change_chart = alt.Chart(change_data).transform_filter(selection).mark_bar().encode(
    x=alt.X('Explained by:N', axis=alt.Axis(title=None)),
    y=alt.Y('Value:Q', axis = alt.Axis(title= None)),
    color='Explained by:N',
    tooltip=['Explained by:N', 'Value:Q']
).properties(
    title='Contributions Change',
    width=400
)


# Combine the lollipop chart with the change chart
combined_chart = lollipop_chart | change_chart

Final_chart = percentage_change & combined_chart
# To display the combined chart in your environment

st.altair_chart(Final_chart, use_container_width=False)
st.write(
    """
    (*) Precovid: Corresponds to the period 2017-2019.

    (*) Covid: Corresponds to the period 2020-2022.
    
    """
)
