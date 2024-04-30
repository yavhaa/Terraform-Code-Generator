import streamlit as st
import pandas as pd
import plotly.express as px
import datetime

from utils import load_data
from config import path_dataset, dimensions_list,metrics_agg,metric_functions
# Set the width of the Streamlit page
st.set_page_config(layout="wide")

# Load data
data = load_data(path_dataset)

# Create a Streamlit app
st.title('Sales and Forecast Time Series')

st.subheader("Time series")
# Add filters
st.sidebar.header('Filters')
filter_selections = {}

# Create filter inputs dynamically
for dimension in dimensions_list:
    filter_selection = st.sidebar.selectbox(f'Select {dimension.capitalize()}',
                                             ["ANY"] + list(data[dimension].unique()) )
    filter_selections[dimension] = filter_selection


# Filter data based on user selections
filtered_data = data.copy()
for dimension, selection in filter_selections.items():
    if selection != 'ANY':
        filtered_data = filtered_data[filtered_data[dimension] == selection]

start_date = st.sidebar.date_input('Start Date', data['date'].min())
end_date = st.sidebar.date_input('End Date', data['date'].max())

# Filter data based on date
filtered_data = filtered_data[
    (filtered_data['date'] >= pd.to_datetime(start_date)) &
    (filtered_data['date'] <= pd.to_datetime(end_date))
]

def first_date_of_month(date):
    return date.replace(day=1)

def first_date_of_week(date):
    return date - datetime.timedelta(days=date.weekday())

def first_date_of_year(date):
    return date.replace(month=1, day=1)

# Dropdown to select time granularity
time_granularity = st.sidebar.selectbox('Select Time Granularity', ['Default granularity', 'Weekly', 'Monthly', 'Yearly'])
filtered_data['date'] = pd.to_datetime(filtered_data['date'])

if time_granularity == 'Weekly':
    filtered_data['current_date'] = filtered_data['date'].apply(first_date_of_week)
elif time_granularity == 'Monthly':
    filtered_data['current_date'] = filtered_data['date'].apply(first_date_of_month)
elif time_granularity == 'Yearly':
    filtered_data['current_date'] = filtered_data['date'].apply(first_date_of_year)
else: 
    filtered_data['current_date'] = filtered_data['date']

# Putting at the right time granularity
filtered_data_time_grouped = filtered_data.groupby(['current_date']+dimensions_list).agg(metrics_agg).reset_index()


# Add an aggregation section
st.sidebar.header('Aggregation')
aggregation_options = st.sidebar.multiselect('Select Aggregation Dimension(s)', ['TOTALS'] + dimensions_list, default=['TOTALS'])
# Apply aggregation if selected

if 'TOTALS' in aggregation_options:
    aggregated_data = filtered_data_time_grouped.groupby(["current_date"]).agg(metrics_agg).reset_index()
    aggregated_data["hue_dimension"] = "TOTALS"
else:
    selected_aggregations = [dim for dim in aggregation_options if dim in dimensions_list]

    if selected_aggregations:
        aggregated_data = filtered_data_time_grouped.groupby(aggregation_options+["current_date"]).agg(metrics_agg).reset_index()

    else:
        aggregated_data = filtered_data_time_grouped.copy()
    aggregated_data['hue_dimension'] = aggregated_data[selected_aggregations].apply(lambda x: ' x '.join(x), axis=1)

st.sidebar.header('Display series')
# Check if data exists after aggregation
if not aggregated_data.empty:
    selected_hue_values = st.sidebar.multiselect('Select Hue Dimension Values',
                                                ['ALL'] + list(aggregated_data['hue_dimension'].unique()),
                                                default=['ALL'])

    # Filter the aggregated_data based on selected 'hue_dimension' values
    if 'ALL' in selected_hue_values:
        filtered_aggregated_data = aggregated_data
    else:
        filtered_aggregated_data = aggregated_data[aggregated_data['hue_dimension'].isin(selected_hue_values)]

    # Create a line chart using Plotly Express with the filtered/aggregated data
    fig = px.line(filtered_aggregated_data, x='current_date', 
                y=['sales', 'forecast'],  # Separate y-values for 'sales' and 'forecast'
                labels={'current_date': 'Date', 'value': 'Sales & Forecast'},
                title=f'Sales vs. Forecast Time Series',
                color="hue_dimension",  # Use 'hue_dimension' for color grouping
                line_dash="variable")  # Separate lines for 'sales' and 'forecast'
    # Display the chart
    st.plotly_chart(fig, use_container_width=True)
    



else:
    st.warning('No data available for the selected filters and aggregation.')


st.subheader("Error metrics")

# Initialize an empty DataFrame to store the final result
result_data_evolution = pd.DataFrame()


def compute_metrics_aggregation(aggregated_data, time_column):
    # Check if aggregation_options is not empty
    if 'TOTALS' in aggregation_options:
        evolution_df_join_columns = [time_column, 'hue_dimension']
        # Calculate and store metrics for TOTALS
        result_data = aggregated_data[['hue_dimension']].drop_duplicates().reset_index(drop=True)
        result_data_evolution = aggregated_data[evolution_df_join_columns].drop_duplicates().reset_index(drop=True)

        for metric_name, metric_function in metric_functions.items():
            metric_result = aggregated_data.groupby(["hue_dimension"]).apply(metric_function).reset_index(drop=True)
            metric_result_evolution = aggregated_data.groupby(evolution_df_join_columns).apply(metric_function).reset_index(drop=True)

            result_data[metric_name] = metric_result
            result_data_evolution[metric_name] = metric_result_evolution
    else:
        evolution_df_join_columns = [time_column, "hue_dimension"] + aggregation_options

        # Calculate and store metrics for non-TOTALS
        result_data = aggregated_data[['hue_dimension'] + aggregation_options].drop_duplicates().reset_index(drop=True)
        result_data_evolution = pd.DataFrame()

        for metric_name, metric_function in metric_functions.items():
            # Calculate metric_result for the current metric
            metric_result = aggregated_data.groupby(["hue_dimension"] + aggregation_options).apply(metric_function).reset_index(drop=True)

            # Calculate metric_result_evolution for the current metric and rename the column
            metric_result_evolution = aggregated_data.groupby(evolution_df_join_columns).apply(metric_function).reset_index().rename(columns={0: metric_name})

            # Concatenate metric_result_evolution with the result_data_evolution
            if result_data_evolution.empty:
                result_data_evolution = metric_result_evolution
            else:
                result_data_evolution = pd.merge(result_data_evolution, metric_result_evolution, on=evolution_df_join_columns, how="inner")

            # Store the metric_result in the result_data DataFrame
            result_data[metric_name] = metric_result
    return result_data, result_data_evolution, evolution_df_join_columns


if aggregation_options:
    result_data, result_data_evolution ,evolution_df_join_columns= compute_metrics_aggregation(aggregated_data, "current_date")


    if not result_data.empty:

        filtered_aggregated_data = aggregated_data[aggregated_data['hue_dimension'].isin(selected_hue_values)]

        # Create a bar chart for Forecast Accuracy using Plotly Express
        fig_forecast_accuracy = px.bar(result_data[result_data['hue_dimension'].isin(selected_hue_values)], x='hue_dimension', y='forecast_accuracy',
                                        labels={'hue_dimension': 'Dimension', 'forecast_accuracy': 'Forecast Accuracy'},
                                        title='Forecast Accuracy by Dimension',
                                        color_discrete_sequence=px.colors.qualitative.Set1)
        
        # Create a bar chart for Bias using Plotly Express
        fig_bias = px.bar(result_data[result_data['hue_dimension'].isin(selected_hue_values)], x='hue_dimension', y='bias',
                        labels={'hue_dimension': 'Dimension', 'bias': 'Bias'},
                        title='Bias by Dimension',
                        color_discrete_sequence=px.colors.qualitative.Set1)
        
        # Display the charts
        st.plotly_chart(fig_forecast_accuracy)
        st.plotly_chart(fig_bias)

        for metric in metric_functions.keys():
            fig = px.line(result_data_evolution[result_data_evolution['hue_dimension'].isin(selected_hue_values)], x='current_date', 
                y=[metric],  # Separate y-values for 'sales' and 'forecast'
                labels={'current_date': 'Date'},
                title=f'{metric} Evolution',
                color="hue_dimension",  # Use 'hue_dimension' for color grouping
                line_dash="variable")  # Separate lines for 'sales' and 'forecast'

            # Display the chart
            st.plotly_chart(fig)


    else:
        st.write("No data available for plotting.")
    
    st.subheader("Raw metrics")
    agg_df_with_metrics = aggregated_data.merge(result_data_evolution, on=evolution_df_join_columns, how='inner')
    st.dataframe(agg_df_with_metrics, use_container_width=True)
        # Create a button to trigger the download
    if st.button('Download CSV'):
        # Generate a link for downloading the CSV file
        csv = agg_df_with_metrics.to_csv(index=False)
        st.download_button(
            label='Click to download CSV',
            data=csv,
            file_name='data.csv',
            key='download-csv'
        )

    aggregated_data['day_number'] = aggregated_data['current_date'].dt.day_name()


    st.subheader("Day Performance")
    _, result_data_evolution_day_number ,_= compute_metrics_aggregation(aggregated_data,'day_number')
    st.write(result_data_evolution_day_number)
