import streamlit as st
import pandas as pd
import os 
import json 
from datetime import datetime
import regions


# Set the width of the Streamlit page
st.set_page_config(layout="wide")

#split the screen into 3 columns
col1, col2, col3 = st.columns([1, 1, 1])



# Provider Configuration
st.header('Provider Configuration')
provider = st.selectbox('Cloud provider', ['AWS', 'Azure', 'Google Cloud'])
region = st.text_input('Region')
auth_method = st.text_input('Authentication method')

# Resource Types
st.header('Resource Types')
compute = st.checkbox('Compute instances')
networking = st.checkbox('Networking')
storage = st.checkbox('Storage')
database = st.checkbox('Database')
containers = st.checkbox('Containers')

# Resource Configuration
st.header('Resource Configuration')
resource_name = st.text_input('Name')
size_capacity = st.text_input('Size/Capacity')
resource_config = st.text_input('Configuration options')

# Networking Configuration
st.header('Networking Configuration')
cidr_block = st.text_input('CIDR block')
security_groups = st.text_input('Security groups')
subnets = st.text_input('Subnets')

# Access Control
st.header('Access Control')
iam_roles = st.text_input('IAM roles (AWS) or RBAC (Azure) configurations')
access_policies = st.text_input('Access policies')

# Monitoring and Logging
st.header('Monitoring and Logging')
monitoring_logging = st.text_input('CloudWatch (AWS), Azure Monitor, etc.')

# Additional Features
st.header('Additional Features')
autoscaling = st.text_input('Autoscaling configurations')
load_balancer = st.text_input('Load balancer configurations')
custom_scripts = st.text_input('Custom scripts or userdata for instances')

# Tags
st.header('Tags')
tags = st.text_input('Key-value pairs for resource tagging')

# Output Configuration
st.header('Output Configuration')
output_config = st.text_input('Terraform output variables')

# Modules
st.header('Modules')
modules = st.text_input('Option to include Terraform modules for reusability and modularity')

# Variables and Parameters
st.header('Variables and Parameters')
variables_parameters = st.text_input('Input fields for any variables or parameters required by the Terraform script')

# Dependencies
st.header('Dependencies')
dependencies = st.text_input('Option to specify resource dependencies and order of creation')

# Backend Configuration
st.header('Backend Configuration')
backend_config = st.text_input('Storage backend for Terraform state files (S3, Azure Blob Storage, etc.)')

if st.button('Generate Terraform Script'):
    # Format user inputs into a string
    prompt = f"""
    Provider: {provider}, Region: {region}, Authentication Method: {auth_method},
    Compute: {compute}, Networking: {networking}, Storage: {storage}, Database: {database}, Containers: {containers},
    Resource Name: {resource_name}, Size/Capacity: {size_capacity}, Resource Configuration: {resource_config},
    CIDR Block: {cidr_block}, Security Groups: {security_groups}, Subnets: {subnets},
    IAM Roles: {iam_roles}, Access Policies: {access_policies},
    Monitoring and Logging: {monitoring_logging},
    Autoscaling: {autoscaling}, Load Balancer: {load_balancer}, Custom Scripts: {custom_scripts},
    Tags: {tags},
    Output Configuration: {output_config},
    Modules: {modules},
    Variables and Parameters: {variables_parameters},
    Dependencies: {dependencies},
    Backend Configuration: {backend_config}
    """
