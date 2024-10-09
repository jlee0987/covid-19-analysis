import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

### Cumulative Rate of Confirmed COVID-19 Cases - by Age Group (2020-2022)
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
plt.ylabel('Mean Cumulative Rate')
plt.xlabel('Year')
plt.xticks(rotation=0)
plt.legend(title='Age Group')
plt.tight_layout()
plt.show()
