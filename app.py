import streamlit as st
import pandas as pd
import os
import plotly.express as px
import json

# Set page configuration
st.set_page_config(page_title="Renewable Energy Dashboard", layout="wide")

st.title('Renewable energy distribution in India')
st.subheader('Installed capacity of Renewable Power (in MW)')

# Load data with proper error handling
try:
    # Try to load the data
    df = pd.read_csv('installed_capacity.csv')
    indian_states = json.load(open('India.json', 'r', encoding='utf-8'))

    # Debug: show success message and file info
    st.success("Select the state(s) of your interest")

except FileNotFoundError:
    st.error("""
    ❌ File not found! Trying to find: installed_capacity.csv, India.json
    """)

    # Debug information
    st.write("Current working directory:", os.getcwd())
    st.write("Files in current directory:", os.listdir('.'))

    st.stop()

# Creating a chloropleth map for installed capacity of renewable power in India
geojson_states = []
for feature in indian_states['features']:
    if 'properties' in feature:
        # Try common property keys for state names
        props = feature['properties']
        state_name = props.get('name')
        if state_name:
            geojson_states.append(state_name)

# print("States in GeoJSON:", geojson_states)
# print("States in CSV:", df['State/Uts'].tolist())

# Removing row with index 38 and 39 from the df

df_filtered_map = df.copy().drop([36, 37])


state_mapping = {'Andhra Pradesh': 'Andhra Pradesh', 'Arunachal Pradesh': 'Arunachal Pradesh',
                 'Assam': 'Assam', 'Bihar': 'Bihar', 'Chhattisgarh': 'Chhattisgarh', 'Goa': 'Goa',
                 'Gujarat': 'Gujarat', 'Haryana': 'Haryana', 'Himachal Pradesh': 'Himachal Pradesh',
                 'Jammu & Kashmir': 'Jammu and Kashmir', 'Jharkhand': 'Jharkhand', 'Karnataka': 'Karnataka',
                 'Kerala': 'Kerala', 'Ladakh': 'Ladakh', 'Madhya Pradesh': 'Madhya Pradesh', 'Maharashtra': 'Maharashtra',
                 'Manipur': 'Manipur', 'Meghalaya': 'Meghalaya', 'Mizoram': 'Mizoram', 'Nagaland': 'Nagaland',
                 'Odisha': 'Orissa', 'Punjab': 'Punjab', 'Rajasthan': 'Rajasthan', 'Sikkim': 'Sikkim',
                 'Tamil Nadu': 'Tamil Nadu', 'Tripura': 'Tripura', 'Uttar Pradesh': 'Uttar Pradesh',
                 'Uttarakhand': 'Uttaranchal', 'West Bengal': 'West Bengal', 'Andaman & Nicobar Islands':
                 'Andaman and Nicobar', 'Chandigarh': 'Chandigarh', 'Dadra and Nagar Haveli and Daman & Diu':
                 'Dādra and Nagar Haveli and Damān and Diu', 'Delhi': 'Delhi', 'Lakshadweep': 'Lakshadweep',
                 'Puducherry': 'Puducherry'}


# Apply the mapping to your CSV data
df_filtered_map['State'] = df_filtered_map['State/Uts'].replace(state_mapping)

# Also add the matched names to GeoJSON properties for plotting
for feature in indian_states['features']:
    geo_name = feature['properties'].get('name')
    if geo_name in state_mapping.values():
        feature['properties']['plotly_name'] = geo_name
    else:
        feature['properties']['plotly_name'] = geo_name

fig = px.choropleth(df_filtered_map,
                    geojson=indian_states,
                    locations='State',
                    featureidkey="properties.plotly_name",
                    color='Total Capacity',  # This refers to your existing column
                    color_continuous_scale="Viridis")

fig.update_geos(
    visible=False,  # Hide base map
    fitbounds='locations',  # Focus on your states
    subunitcolor='lightgray',  # State border color
    subunitwidth=0.5)  # State border width

fig.update_coloraxes(colorbar_title="Installed Capacity (MW)",
                     colorscale='Greens')


fig.update_layout(
    title_text='Overview: Renewable Power Installed Capacity',
    title_x=0.5,
    margin=dict(l=0, r=0, t=50, b=0),  # Remove side margins
    height=700,  # Comfortable height
    autosize=False,
    dragmode=False)

st.plotly_chart(fig, use_container_width=True)
# print("Map saved as 'india_renewable_energy_map.html'")

# Continue with your original code
df = df.fillna(0)
df_copy = df.copy()

States = df_copy['State/Uts'].tolist()
selected_states = st.multiselect(
    'Select States', options=States, default=[])
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

