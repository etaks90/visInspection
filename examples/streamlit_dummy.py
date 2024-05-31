import streamlit as st
import pandas as pd
import plotly.express as px
import datetime

# Data dictionary
data = {
    'eventDate': ['2021-01-01 14:23', '2021-01-01 14:24', '2021-01-02 15:25', '2021-01-02 15:35', '2021-01-02 15:45', '2022-01-02 15:35', '2022-01-02 15:45'],
    'pred': ['A', 'A', 'B', 'A', 'B', 'A', 'B'],
    'path': ['X', 'Y', 'Z', 'X', 'Y', 'X', 'Y']
}

# Convert to DataFrame
df = pd.DataFrame(data)
df['eventDate'] = pd.to_datetime(df['eventDate'])

# Set up the Streamlit app
st.title('Event Data Visualization')

# Add separate date inputs for start and end dates
st.subheader('Select Start Date')
start_date = st.date_input("Start Date", value=df['eventDate'].min().date(), min_value=df['eventDate'].min().date(), max_value=df['eventDate'].max().date())


st.subheader('Select End Date')
end_date = st.date_input("End Date", value=df['eventDate'].max().date(), min_value=df['eventDate'].min().date(), max_value=df['eventDate'].max().date() + datetime.timedelta(days=7))

# Convert to datetime.date for filtering if not already
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Ensure end date is after start date
if start_date > end_date:
    st.error('Error: End date must be after start date.')
else:
    # Filter data based on the selected date range
    df_filtered = df[(df['eventDate'] >= start_date) & (df['eventDate'] <= end_date)]

    # Interactive filter for the chart
    selected_preds = st.multiselect('Select Prediction Types', options=df_filtered['pred'].unique(), default=df_filtered['pred'].unique())

    # Filter data based on selection
    filtered_data = df_filtered[df_filtered['pred'].isin(selected_preds)]

    # Display filtered data as a table
    st.subheader('Filtered Data Table')
    st.write(df_filtered)

    # Plotting
    st.subheader('Interactive Event Timeline')

    # Using Plotly for an interactive line chart
    fig = px.scatter(filtered_data, x='eventDate', y='pred', color='pred', labels={'pred': 'Prediction'}, title='Filtered Event Timeline by Prediction')
    st.plotly_chart(fig)
