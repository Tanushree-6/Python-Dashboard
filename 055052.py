import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Load the dataset
hts = pd.read_csv('C:/FORE/Term 1/Imports_Exports_Dataset.csv')

# Convert the 'Date' column to datetime format if not already converted
hts['Date'] = pd.to_datetime(hts['Date'], errors='coerce')

# Define categorical and numerical variables
categorical_options = ['Country', 'Product', 'Import_Export', 'Category', 'Port', 'Shipping_Method', 'Supplier', 'Customer', 'Payment_Terms']
numeric_options = ['Quantity', 'Value', 'Weight']

# Streamlit dashboard setup
st.title("Imports and Exports Dashboard")

# Sidebar for filters
st.sidebar.header("Filters")

# Filter to choose charts to display
chart_type = st.sidebar.multiselect(
    "Select Chart Types to Display",
    options=['Pie Chart', 'Bar Chart', 'Line Chart', 'Scatter Plot', 'Box Plot', 'Heatmap', 'Histogram'],
    default=['Pie Chart', 'Bar Chart', 'Line Chart', 'Scatter Plot', 'Box Plot', 'Heatmap', 'Histogram']
)

# Date range filter
min_date = hts['Date'].min()
max_date = hts['Date'].max()
date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date])

# Filter dataset by selected date range only
hts_filtered = hts[(hts['Date'] >= pd.Timestamp(date_range[0])) & (hts['Date'] <= pd.Timestamp(date_range[1]))]

# Pie Chart for Shipping Method and Category
if 'Pie Chart' in chart_type:
    st.header("Pie Chart - Shipping Method and Category Distribution")
    pie_chart = px.pie(hts_filtered, names='Shipping_Method', title="Shipping Method Distribution", color_discrete_sequence=px.colors.qualitative.Vivid)
    st.plotly_chart(pie_chart)

    pie_chart_category = px.pie(hts_filtered, names='Category', title="Category Distribution", color_discrete_sequence=px.colors.qualitative.Vivid)
    st.plotly_chart(pie_chart_category)

# Bar Plot for Payment Terms and Import/Export
if 'Bar Chart' in chart_type:
    st.header("Bar Chart - Payment Terms and Import/Export Distribution")
    
    bar_chart_payment_terms = px.bar(hts_filtered, x='Payment_Terms', title="Payment Terms Distribution", color='Payment_Terms', color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(bar_chart_payment_terms)

    bar_chart_import_export = px.bar(hts_filtered, x='Import_Export', title="Import/Export Distribution", color='Import_Export', color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(bar_chart_import_export)

# Line Chart for Import/Export over Time
if 'Line Chart' in chart_type:
    st.header("Line Chart for Import and Export Over Time")
    hts_filtered['Year'] = hts_filtered['Date'].dt.year  # Extract year from the date
    import_export_summary = hts_filtered.groupby(['Year', 'Import_Export']).agg({'Quantity': 'sum'}).reset_index()

    line_chart = px.line(import_export_summary, x='Year', y='Quantity', color='Import_Export', title="Imports and Exports Over Time", markers=True, color_discrete_sequence=px.colors.qualitative.Bold)
    st.plotly_chart(line_chart)

# Scatter Plot for Quantity vs Value
if 'Scatter Plot' in chart_type:
    st.header("Scatter Plot of Quantity vs Value")
    scatter_chart = px.scatter(hts_filtered, x='Quantity', y='Value', title="Scatter Plot of Quantity vs Value", color='Import_Export', color_discrete_sequence=px.colors.qualitative.Prism)
    st.plotly_chart(scatter_chart)

# Box Plot for Value Distribution by Shipping Method
if 'Box Plot' in chart_type:
    st.header("Box Plot - Value Distribution by Shipping Method")
    box_plot = px.box(hts_filtered, x='Shipping_Method', y='Value', title="Value Distribution by Shipping Method", color='Shipping_Method', color_discrete_sequence=px.colors.qualitative.Set3)
    st.plotly_chart(box_plot)

# Heatmap - Correlation of Selected Numeric Variables
if 'Heatmap' in chart_type:
    st.header("Heatmap - Correlation of Numeric Variables")
    correlation_matrix = hts_filtered[numeric_options].corr()
    heatmap = go.Figure(data=go.Heatmap(
        z=correlation_matrix.values,
        x=numeric_options,
        y=numeric_options,
        colorscale='Viridis'))

    heatmap.update_layout(title="Heatmap of Numeric Variables", xaxis_title="Variables", yaxis_title="Variables")
    st.plotly_chart(heatmap)

# Histogram for Selected Numeric Variable
if 'Histogram' in chart_type:
    st.header("Histogram of Selected Numeric Variable")
    selected_histogram_var = st.sidebar.selectbox("Select Numeric Variable for Histogram", numeric_options)
    histogram = px.histogram(hts_filtered, x=selected_histogram_var, nbins=30, title=f'Histogram of {selected_histogram_var}', color_discrete_sequence=px.colors.qualitative.Safe)
    st.plotly_chart(histogram)
