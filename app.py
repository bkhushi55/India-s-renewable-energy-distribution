import streamlit as st
import pandas as pd
import os
import plotly.express as px

# Set page config first (should be the first Streamlit command)
st.set_page_config(page_title="Renewable Energy Dashboard", layout="wide")

st.title('Renewable energy distribution in India')
st.subheader('Installed capacity of Renewable Power (in MW)')

# Load data with proper error handling
try:
    # Try to load the data
    df = pd.read_csv('installed_capacity.csv')

    # Debug: show success message and file info
    st.success("✅ Data loaded successfully!")

except FileNotFoundError:
    st.error("""
    ❌ File not found! Trying to find: installed_capacity.csv
    """)

    # Debug information
    st.write("Current working directory:", os.getcwd())
    st.write("Files in current directory:", os.listdir('.'))

    st.stop()

# Continue with your original code
df = df.fillna(0)
df_copy = df.copy()

States = df_copy['State/Uts'].tolist()
selected_states = st.multiselect(
    'Select States', options=States, default=States)
done_clicked = st.button('Done')

filtered_df = df_copy[df_copy['State/Uts'].isin(selected_states)]

if done_clicked:
    st.write('Data as on 30.06.2025')
    st.dataframe(filtered_df)

    # Plotting the data
    fig = px.bar(filtered_df, x='State/Uts', y=filtered_df.columns[1:],
                 title='Installed Capacity of Renewable Power',
                 labels={
                     'value': 'Installed Capacity (MW)', 'variable': 'Renewable Energy Type'},
                 barmode='group')
    st.plotly_chart(fig, use_container_width=True)

