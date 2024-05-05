import streamlit as st
import pandas as pd
import os 
import json 
from datetime import datetime
import regions
import requests
from hello import get_code

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
    col1.markdown("&nbsp;")
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

    
    col1.markdown("&nbsp;")
    col1.markdown("&nbsp;")
    col1.markdown("&nbsp;")

    region = col1.selectbox("Region", Regions)
    col1.markdown("&nbsp;")
    col1.markdown("&nbsp;")
    col1.markdown("&nbsp;")

    col1.header("Resource Details")
    resource_group = col1.text_input("Resource Group")
    vnet = col1.text_input("VNet")
    CIDR = col1.text_input("CIDR")
    subnet_name = col1.text_input("Subnet")
    subnet_CIDR = col1.text_input("Subnet CIDR")
    security_group = col1.text_input("Security Group")


    col2.markdown("&nbsp;")

    col2.header("Instance Details")
    instance_type = col2.selectbox("Instance Type", instances)
    col2.markdown("&nbsp;")
    col2.markdown("&nbsp;")
    col2.markdown("&nbsp;") 
    instance_count = col2.number_input("Instance Count", min_value=1, value=1, step=1)
    col2.markdown("&nbsp;")
    col2.markdown("&nbsp;")
    col2.markdown("&nbsp;")

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
            "CIDR": CIDR,
            "subnet_name": subnet_name,
            "subnet_CIDR": subnet_CIDR,
            "security_group": security_group,
            "instance_type": instance_type,
            "instance_count": instance_count,
            "storage_account": storage_account,
            "database_name": database_name,
            "database_type": database_type,
            "database_size": database_size,
            "database_count": database_count,
        }

        # Create a prompt out of the template configuration
        prompt=f''' Write a Terraform script to provision an infrastructure with the following configuration:

1. Provider Configuration:
   - Use the `{provider}` provider.
   - Set the region to `{region}`.

2. VPC Creation:
   - Define a VPC named `{vnet}`.
   - Assign the CIDR block `{CIDR}`.

3. Subnet Creation:
   - Create a subnet:
     - Name: `{subnet_name}`.
     - CIDR block: `{subnet_CIDR}`.
     - Availability Zone: `{region}`.

4. Internet Gateway Creation:
   - Create an internet gateway named `{vnet}_igw`.
   - Attach the internet gateway to the VPC.

5. Route Table Creation:
   - Define a route table named `{vnet}_route_table` associated with the VPC.
   - Add a route to `0.0.0.0/0` via the internet gateway.

6. Route Table Association:
   - Associate the route table with the subnet.

7. Security Group Creation:
   - Create a security group named `{security_group}`.
   - Allow inbound traffic on port 22 (SSH) from anywhere.
   - Allow all outbound traffic.

8. Instance Creation:
   - Launch an instance named `{template_name}`.
   - Use the `{instance_type}` instance type.
   - Place the instance in `{subnet_name}`.
   - Associate the instance with the `{security_group}` security group.
   - Apply a tag with the key `Name` and the value `{template_name}`.

9. Storage Account Creation:
   - Create a storage account named `{storage_account}`.

10. Database Creation:
   - Create a `{database_type}` database named `{database_name}`.
   - Set the size to `{database_size}`.
   - Create `{database_count}` number of databases.

Ensure proper dependencies and attribute references are used.'''
       

        # Print the prompt
        print(prompt)
        response=get_code(prompt)
        print(response)



        # Save the template information to a JSON file
        with open("templates/template_config.json", "w") as f:
            json.dump(template_config, f)
        st.write("Template saved successfully!")


    return template_config
    
# Sidebar with buttons
st.sidebar.title("Template Management")
# Create a selectbox in the sidebar to choose an action
selected_action = st.sidebar.selectbox("Select Action", ["Create New Template", "List Available Templates"])

create_edit_template()


    
    
    
    
