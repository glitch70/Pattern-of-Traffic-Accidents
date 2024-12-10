import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# Load data
data_filepath = 'US_Accidents_March23.csv'
df = pd.read_csv(data_filepath)

# Data cleaning and preprocessing
df.dropna(thresh=0.5, axis=1, inplace=True)  # Drop columns with more than 50% missing values
df.drop(['ID', 'End_Lng', 'End_Lat', 'Number'], axis=1, inplace=True)  # Drop unnecessary columns

# Convert Start_Time to datetime format
df['Start_Time'] = pd.to_datetime(df['Start_Time'], errors='coerce')

# Extract year, month, hour, and weekday from Start_Time
df['Year'] = df['Start_Time'].dt.year
df['Month'] = df['Start_Time'].dt.month
df['Hour'] = df['Start_Time'].dt.hour
df['Weekday'] = df['Start_Time'].dt.weekday

# Plotting countplot for states
plt.figure(figsize=(20, 5))
sns.countplot(x='State', data=df, order=df['State'].value_counts().index[:25], palette='crest')
plt.title('States with Highest Number of Accidents')
plt.xlabel('State')
plt.ylabel('Number of Accidents')
plt.xticks(rotation=45)
plt.show()

# Plotting countplot for top 50 cities with highest number of accidents
plt.figure(figsize=(20, 5))
sns.countplot(x='City', data=df, order=df['City'].value_counts().index[:50], palette='crest')
plt.title('Top 50 Cities with Highest Number of Accidents')
plt.xlabel('City')
plt.ylabel('Number of Accidents')
plt.xticks(rotation=90)
plt.show()

# Plotting distribution of accidents by month for the year 2016
plt.figure(figsize=(10, 5))
sns.countplot(x='Month', data=df[df['Year'] == 2016], palette='crest')
plt.title('Number of Accidents by Month - 2016')
plt.xlabel('Month')
plt.ylabel('Number of Accidents')
plt.show()

# Plotting distribution of accidents by month for the year 2020
plt.figure(figsize=(10, 5))
sns.countplot(x='Month', data=df[df['Year'] == 2020], palette='crest')
plt.title('Number of Accidents by Month - 2020')
plt.xlabel('Month')
plt.ylabel('Number of Accidents')
plt.annotate('Covid-19 Pandemic', xy=(2, 150000), fontsize=12)
plt.annotate("[", xy=(0, 0), xytext=(1.9, 150000), arrowprops={'arrowstyle': '-|>'}, fontsize=12)
plt.annotate("]", xy=(10, 0), xytext=(4.5, 150000), arrowprops={'arrowstyle': '-|>'}, fontsize=12)
plt.show()

# Plotting distribution of accidents by hour of day
plt.figure(figsize=(10, 5))
sns.histplot(df['Start_Time'].dt.hour, bins=24, stat='density')
plt.title('Distribution of Accidents by Hour of Day')
plt.xlabel('Hour of Day')
plt.ylabel('Density')
plt.show()

# Plotting pie chart for day/night distribution of accidents
plt.figure(figsize=(6, 6))
df['Sunrise_Sunset'].value_counts().plot(kind='pie', autopct="%.1f%%", explode=[0.01]*len(df['Sunrise_Sunset'].value_counts()), pctdistance=0.5)
plt.title('Day/Night Distribution of Accidents')
plt.ylabel('')
plt.show()

# Plotting scatter plot for latitude and longitude with severity color coding
plt.figure(figsize=(20, 15))
sns.scatterplot(x='Start_Lng', y='Start_Lat', hue='Severity', data=df, palette='viridis')
plt.title('Accident Distribution by Latitude and Longitude with Severity')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()

# Plotting pie chart for severity levels
severe_accidents_4 = df[df['Severity'] == 4]['State'].value_counts()
severe_accidents_3 = df[df['Severity'] == 3]['State'].value_counts()
severe_accidents_2 = df[df['Severity'] == 2]['State'].value_counts()
severe_accidents_1 = df[df['Severity'] == 1]['State'].value_counts()

fig, ax = plt.subplots(2, 2, figsize=(20, 20))

# Severity 1
ax[0, 0].pie(severe_accidents_1, labels=severe_accidents_1.index, autopct='%1.1f%%')
ax[0, 0].set_title("Least Severe Accidents: Severity=1")

# Severity 2
ax[0, 1].pie(severe_accidents_2, labels=severe_accidents_2.index, autopct='%1.1f%%')
ax[0, 1].set_title("Less Severe Accidents: Severity=2")

# Severity 3
ax[1, 0].pie(severe_accidents_3, labels=severe_accidents_3.index, autopct='%1.1f%%')
ax[1, 0].set_title("Moderate Severe Accidents: Severity=3")

# Severity 4
ax[1, 1].pie(severe_accidents_4, labels=severe_accidents_4.index, autopct='%1.1f%%')
ax[1, 1].set_title("Most Severe Accidents: Severity=4")

plt.tight_layout()
plt.show()

# Choropleth map for state-wise accidents
state_counts = df['State'].value_counts()

fig = go.Figure(data=go.Choropleth(
    locations=state_counts.index,
    z=state_counts.values.astype(float),
    locationmode="USA-states",
    colorscale="turbo",
))

fig.update_layout(
    title_text="Number of Accidents for each State",
    geo_scope="usa",
)

fig.show()

# Print unique state codes and total number of states
print("State Code: ", df['State'].unique())
print("Total No. of States in Dataset: ", len(df['State'].unique()))
