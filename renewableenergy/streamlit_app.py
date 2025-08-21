import streamlit as st
import os
import pandas as pd
import plotly.express as px

base_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(
    base_dir, 'data', 'State-wise (Location based) installed capacity of Renewable Power as on 30.06.2025.csv')

df = pd.read_csv(data_path)
# print(df.head(5))

# # df.info()

# # Changing nan values to zero for states with no installed capacity for columns 1 to -1
df = df.fillna(0)
# print(df.head(5))
df_copy = df.copy()
st.title('Renewable energy distribution in India')
st.subheader(
    'Installed capacity of Renewable Power (in MW)')
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
