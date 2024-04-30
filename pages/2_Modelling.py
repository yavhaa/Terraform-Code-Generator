import streamlit as st
import pandas as pd
import os 
import json 
from datetime import datetime
import regions
import requests

# Set the width of the Streamlit page
st.set_page_config(layout="wide")

#split the screen into 3 columns
col1, col2, col3 = st.columns([1, 1, 1])



def create_edit_template(template_config={}):
    # Define a list of available model types
    Providers = ["Azure", "AWS", "GCP"]

    # Create a Streamlit page
    st.title("infrastructure Configuration")
    st.write("This page allows you to create or edit a template for infrastructure configuration.")
    st.write("Please fill out the form below to create or edit a template.")

    # Create a form to collect the template information
    template_name = st.text_input("Template Name", template_config.get("template_name", ""))
    # Create columns for better organization
    col1, col2 = st.columns(2)

    # Group related inputs into sections
    col1.header("Provider Details")
    provider = col1.selectbox("Provider", Providers)

    #for each provider selected, display a select box with the available regions
    if provider == "Azure":
        Regions = regions.azure_regions
    elif provider == "AWS":
        Regions = regions.aws_regions
    elif provider == "GCP":
        Regions = regions.gcp_regions

    
    #for each provider selected, display a select box with the available instance types
    if provider == "Azure":
        instances = regions.azure_instance_types
    elif provider == "AWS":
        instances = regions.aws_instance_types
    elif provider == "GCP":
        instances = regions.gcp_instance_types
    

    #for each provider selected, display a select box with the available database types
    if provider == "Azure":
        Database_Types = regions.azure_database_types
    elif provider == "AWS":
        Database_Types = regions.aws_database_types
    elif provider == "GCP":
        Database_Types = regions.gcp_database_types

    
    

    region = col1.selectbox("Region", Regions)

    col1.header("Resource Details")
    resource_group = col1.text_input("Resource Group")
    vnet = col1.text_input("VNet")
    subnet = col1.text_input("Subnet")
    security_group = col1.text_input("Security Group")

    col2.header("Instance Details")
    instance_type = col2.selectbox("Instance Type", instances)
    instance_count = col2.number_input("Instance Count", min_value=1, value=1, step=1)

    col2.header("Storage Details")
    storage_account = col2.text_input("Storage Account")

    col2.header("Database Details")
    database_name = col2.text_input("Database Name")
    database_type = col2.selectbox("Database Type", Database_Types)
    database_size = col2.text_input("Database Size")
    database_count = col2.number_input("Database Count", min_value=1, value=1, step=1)

    submit = st.button("Submit")
    # If the user clicks the submit button, save the template information
    if submit:
        template_config = {
            "template_name": template_name,
            "provider": provider,
            "region": region,
            "resource_group": resource_group,
            "vnet": vnet,
            "subnet": subnet,
            "security_group": security_group,
            "instance_type": instance_type,
            "instance_count": instance_count,
            "storage_account": storage_account,
            "database_name": database_name,
            "database_type": database_type,
            "database_size": database_size,
            "database_count": database_count,
        }
    
    return template_config
    
# Sidebar with buttons
st.sidebar.title("Template Management")
# Create a selectbox in the sidebar to choose an action
selected_action = st.sidebar.selectbox("Select Action", ["Create New Template", "List Available Templates"])

create_edit_template()


    
    
    
    
