import os
import streamlit as st
import pandas as pd
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import prompts

# OpenAI API
_ = load_dotenv(find_dotenv())
client = OpenAI(api_key="<API_KEY")
model = "gpt-3.5-turbo"
temeperature = 0.4
max_tokens = 1

# prompts
systeme_message = prompts.system_message
prompt = prompts.generate_prompt("generate terraform code")


def get_code(prompt):
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": systeme_message},
            {"role": "user", "content": prompt},
        ],
        temperature=temeperature,
        max_tokens=max_tokens,
    )
    return completion.choices[0].message.content


#streamlit
st.set_page_config(layout="wide")
st.title('Terraform Code Generator')

#split the screen into 3 columns, first column for the user input, second column for the chatbot response, and the third column for 2 dropdown lists containing the available providers and resources

col1, col2, col3 = st.columns([2, 5, 3])

#user input
# Python
with col2:
    st.write("Chatbot Response:")
with col1:
    
    user_input = st.text_area('Enter your terraform code here:',height=200)
    if st.button('Generate Terraform Code'):
        completion = get_code(user_input)
        with col2:
            st.write('Chatbot Response:')
            st.code(completion, language='hcl')



#dropdown lists

with col3:
    providers = st.selectbox('Select the provider:', ['aws', 'azure', 'google'])
    resources = st.selectbox('Select the resource:', ['vpc', 'subnet', 'instance', 'bucket', 'database'])








# if __name__ == "__main__":
#     while True:
#         user_input = user_input
#         if user_input.lower() in ["quit", "exit", "bye"]:
#             break
#         completion = get_code(user_input)
#         print("chatbot: ", completion)
