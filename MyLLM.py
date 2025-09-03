import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from openai import OpenAI

# Load environment variables from .env file
load_dotenv(override=True)

api_key = os.getenv('MM_API_Key')

# Validate API key
if not api_key:
    print("No API key was found - check your .env file!")
elif not api_key.startswith("sk-"):
    print("API key format incorrect - check your .env file!")
else:
    print("API key loaded successfully!")
#
openai = OpenAI(api_key=api_key)
#
# # A function to read all files in a directory and return their contents
def read_files_in_folder(folder_path, max_chars=5000):
    file_contents = {}
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding="utf-8", errors="ignore") as file:
                content = file.read()[:max_chars]
                file_contents[filename] = content
    return file_contents

# Function to generate a system prompt for summarization
system_prompt = "You are an AI assistant that analyzes only the files related to the query and provides useful insights. Do not use an"
#Summarize only the first 2 files and answer user queries based on their contents."

# Function to generate messages for OpenAI API
def messages_for_files(files):
    file_texts = "\n\n".join([f"### {name} ###\n{content}" for name, content in files.items()])
    user_prompt = f"Provide a useful summary for the files in {file_texts} i"

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

# Function to summarize folder contents
def summarize_folder(folder_path):
    files = read_files_in_folder(folder_path)
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages_for_files(files)
    )
    return response.choices[0].message.content

# Function to answer user queries based on the files
def query_folder(folder_path, user_question):
    files = read_files_in_folder(folder_path)
    messages = messages_for_files(files)
    messages.append({"role": "user", "content": user_question})

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
    return response.choices[0].message.content

# Example usage
folder_path = "C:/Books"  # Change this to your folder path
# print("Summarizing folder contents:")
# print(summarize_folder(folder_path))
userQuery = input("Enter your query: ")
print("\nAnswering a user query:")
print(query_folder(folder_path,  userQuery))

## --------------------------------------------------------------------------------------------------------------------
## COT prompting technique
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
template = """Question: {question} Answer: Let's think step by step."""
prompt = ChatPromptTemplate.from_template(template)
model = OllamaLLM(model="llama3.1")
chain = prompt | model
resp = chain.invoke({"question":"What is LangChain"})
print(resp)


