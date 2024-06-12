import os
import streamlit as st
import pandas as pd
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import prompts

# OpenAI API
load_dotenv()  # take environment variables from .env.
api_key = os.getenv("api_key")
client = OpenAI(api_key=api_key)
model = "gpt-4-turbo"
temeperature = 0.4
#adjust this before each run if needed
max_tokens = 500


# def get_code(prompt):
#     response=client.completions.create(
#         model=model,
#         prompt=prompt,
#         temperature=temeperature,
#         max_tokens=max_tokens,
#     )
#     return response.choices[0].text

    

# prompts
# systeme_message = prompts.system_message
# prompt = prompts.generate_prompt("generate terraform code")


def get_code(prompt):
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "you are a Terraform code generator, and you estimate the costs of cloud infrastructure. You generate consize code and estimation"},
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
