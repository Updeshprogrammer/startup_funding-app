import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
@st.cache
def load_data():
    data = pd.read_csv('startup_cleaned.csv')
    data['date'] = pd.to_datetime(data['date'])
    return data

data = load_data()

# Title
st.title('Startup Funding Analysis')

# Display raw data
if st.checkbox('Show raw data'):
    st.write(data)

# Filter by date
st.sidebar.header('Filter by Date')
start_date = st.sidebar.date_input('Start date', data['date'].min())
end_date = st.sidebar.date_input('End date', data['date'].max())

filtered_data = data[(data['date'] >= pd.to_datetime(start_date)) & (data['date'] <= pd.to_datetime(end_date))]

# Filter by city
cities = st.sidebar.multiselect('Select cities', options=data['city'].unique(), default=data['city'].unique())
filtered_data = filtered_data[filtered_data['city'].isin(cities)]

# Filter by round
rounds = st.sidebar.multiselect('Select funding rounds', options=data['round'].unique(), default=data['round'].unique())
filtered_data = filtered_data[filtered_data['round'].isin(rounds)]

# Display filtered data
st.write(filtered_data)

# Visualization
st.header('Visualizations')

# Funding amount over time
st.subheader('Funding amount over time')
fig, ax = plt.subplots()
filtered_data.groupby('date')['amount'].sum().plot(ax=ax)
st.pyplot(fig)

# Top cities by funding amount
st.subheader('Top cities by funding amount')
top_cities = filtered_data.groupby('city')['amount'].sum().sort_values(ascending=False)
st.bar_chart(top_cities)

# Top startups by funding amount
st.subheader('Top startups by funding amount')
top_startups = filtered_data.groupby('startup')['amount'].sum().sort_values(ascending=False).head(10)
st.bar_chart(top_startups)

# Top investors by number of investments
st.subheader('Top investors by number of investments')
top_investors = filtered_data['investors'].value_counts().head(10)
st.bar_chart(top_investors)
