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
max_tokens = 200

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











# if __name__ == "__main__":
#     while True:
#         user_input = user_input
#         if user_input.lower() in ["quit", "exit", "bye"]:
#             break
#         completion = get_code(user_input)
#         print("chatbot: ", completion)
