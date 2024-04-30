import streamlit as st
import pandas as pd
import os 
import json 
from datetime import datetime
from pages import regions
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
    provider = st.selectbox("Provider", Providers)

    #for each provider selected, display a select box with the available regions
    if provider == "Azure":
        Regions = regions.azure_regions
    elif provider == "AWS":
        Regions = regions.aws_regions

    elif provider == "GCP":
        Regions = regions.gcp_regions
    region = st.selectbox("Region", Regions)


    resource_group = st.text_input("Resource Group")
    vnet = st.text_input("VNet")
    subnet = st.text_input("Subnet")
    security_group = st.text_input("Security Group")
    instance_type = st.text_input("Instance Type")
    instance_count = st.text_input("Instance Count")
    storage_account = st.text_input("Storage Account" )
    database_name = st.text_input("Database Name")
    database_type = st.text_input("Database Type")
    database_size = st.text_input("Database Size")
    database_count = st.text_input("Database Count")
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


    
    
    
    
