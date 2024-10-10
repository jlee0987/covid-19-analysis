import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

### 1 - Mean Cumulative Rate of Confirmed COVID-19 Cases - by Age Group (2020-2022)
# Reading the CSV file
df = pd.read_csv("/Users/jillianlee/Downloads/COVID_19_Cases_and_Deaths_Ottawa.csv")

# Extracting the year from the Date column and filtering for the years 2020-2022
df['year'] = pd.to_datetime(df['Date'], errors='coerce').dt.year
df = df[df['year'].isin([2020, 2021, 2022])]

# Rearranging columns
titles = list(df.columns)
titles[0], titles[34] = titles[34], titles[0]
df = df[titles]
df

# Selecting relevant columns for the analysis
df2 = df.iloc[:, [0] + list(range(15, 25))]
df2

# Calculating the mean cumulative rate of confirmed cases by year
df3 = df2.groupby('year', as_index=False).mean(numeric_only=True)
df3

# Defining age group categories
age_groups = {
    '0-14': ['Cumulative_Rate_for_0_9_Years__', 'Cumulative_Rate_for_10_19_Years'],
    '15-24': ['Cumulative_Rate_for_20_29_Years'],
    '25-64': ['Cumulative_Rate_for_30_39_Years', 
              'Cumulative_Rate_for_40_49_Years', 
              'Cumulative_Rate_for_50_59_Years'],
    '65 and up': ['Cumulative_Rate_for_60_69_Years', 
                  'Cumulative_Rate_for_70_79_Years', 
                  'Cumulative_Rate_for_80_89_Years', 
                  'Cumulative_Rate_for_90_Years_an']
}

# Creating a DataFrame to store the mean values for the age groups
age_group_dataframe = pd.DataFrame({group: df3[columns].mean(axis=1) for group, columns in age_groups.items()})
age_group_dataframe['year'] = df3['year']

# Plotting the bar charts
age_group_dataframe.set_index('year').plot(kind='bar', figsize=(12, 6))
plt.title('Mean Cumulative COVID-19 Rates by Age Group (2020-2022)')
plt.ylabel('Mean Cumulative Rate (per 100,000)')
plt.xlabel('Year')
plt.xticks(rotation=0)
plt.legend(title='Age Group')
plt.tight_layout()
plt.show()



### 2 - Mean Cumulative Rate of Confirmed COVID-19 Cases - by Gender (2020-2022)

# Selecting relevant columns for the analysis
df2 = df.iloc[:, [0] + list(range(25,27))]
df2

# Calculating the mean cumulative rates by year
df3 = df2.groupby('year', as_index=False).mean(numeric_only=True)
df3

# Setting up the bar chart
plt.figure(figsize=(10, 6))

# Parameters
bar_width = 0.35
x_indices = range(len(df3['year']))

# Plotting the bar chart
bars_male = plt.bar(x_indices, df3['Cumulative_Rate_for_Males__per_'], width=bar_width, color='#0000FF', label='Male', align='center')
bars_female = plt.bar([x + bar_width for x in x_indices], df3['Cumulative_Rate_for_Females__pe'], width=bar_width, color='#FF00FF', label='Female', align='center')

# Adding value labels above the bars
for bars in [bars_male, bars_female]:
    for bar in bars:
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), 
                 round(bar.get_height(), 2), ha='center', va='bottom')

# Chart annotations
plt.title('Mean Cumulative COVID-19 Rates by Gender (2020-2022)')
plt.xlabel('Year')
plt.ylabel('Mean Cumulative Rate (per 100,000)')
plt.xticks(x_indices, df3['year'], rotation=45)
plt.legend()
plt.tight_layout()
plt.show()



### 3 - Hospitalization Rates (2020-2023)

# Ensuring the 'Date' column is in datetime format
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# Excluding rows with empty data
data = df.dropna(subset=['Cases_Currently_in_Hospital', 'Total_Active_Cases_by_Date'])

# Resampling the data to every 3 months
data.set_index('Date', inplace=True)
df2 = data.resample('3ME').last()

# Calculating the Hospitalization Rate and dropping NaNs
df2['Hospitalization_Rate'] = df2['Cases_Currently_in_Hospital'] / df2['Total_Active_Cases_by_Date'] * 100
df2.dropna(subset=['Hospitalization_Rate'], inplace=True)

plt.figure(figsize=(10, 5))
plt.plot(df2.index, df2['Hospitalization_Rate'], label='Hospitalization Rate (%)', color='blue')
plt.title('Hospitalization Rate Over Time (2020-2023)')
plt.xlabel('Date')
plt.ylabel('Hospitalization Rate (%)')

# Customizing the x-ticks to show every three months only
plt.xticks(pd.date_range(start='2020-01-01', end='2023-12-31', freq='3MS'), 
           rotation=45, 
           ha='right')

plt.tight_layout()
plt.show()



### 4 - Top 5 Days with the Most Active Cases (2020-2024)

# Extracting the date from the Date column
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# Filtering for the years 2020 to 2024
df = df[(df['Date'].dt.year >= 2020) & (df['Date'].dt.year <= 2024)]

# Creating df2 with the relevant columns
df2 = df[['Date','Total_Active_Cases_by_Date']]

# Grouping by Date and summing up active cases
total_cases_by_date = df2.groupby('Date')['Total_Active_Cases_by_Date'].sum()

# Getting the top 5 days
top_5 = total_cases_by_date.nlargest(5).reset_index()

# Plotting the horizontal bar chart with seaborn
import seaborn as sns
bar_plot = sns.barplot(x='Total_Active_Cases_by_Date', y='Date', data=top_5)

# Adding value labels
for index, value in enumerate(top_5['Total_Active_Cases_by_Date']):
    bar_plot.text(value, index, str(value), color='black', ha='left', va='center')

plt.title('Top 5 Days with the Most Active Cases (2020-2024)')
plt.xlabel('Total Active Cases by Date')
plt.ylabel('Date')
plt.show()

          

### 5 - Time Series Plot - Cumulative Deaths (2020-2024)

# Extracting the date from the Date column
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# Filtering for the years 2020 to 2024
df = df[(df['Date'].dt.year >= 2020) & (df['Date'].dt.year <= 2024)]

# Creating df2 with the relevant columns
df2 = df[['Date', 'Cumulative_Deaths_by_Date_of_De']]

# Resampling the data to every 3 months
df2.set_index('Date', inplace=True)
df2 = df2.resample('3ME').last()

# Plotting the time series data
plt.figure(figsize=(12, 6))
plt.plot(df2.index, df2['Cumulative_Deaths_by_Date_of_De'], marker='o', linestyle='-', color='b')

# Adding titles and labels
plt.title('Cumulative COVID-19 Deaths in Ottawa (2020-2024)')
plt.xlabel('Date')
plt.ylabel('Cumulative Deaths')
plt.xticks(rotation=45)

# Customizing the x-ticks to display data for every three months
plt.xticks(pd.date_range(start='2020-01-01', end='2024-12-31', freq='3MS'), 
           rotation=45, 
           ha='right')

plt.grid()
plt.tight_layout()
plt.show()
