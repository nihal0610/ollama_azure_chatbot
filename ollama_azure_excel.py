#ollama_azure_chatbot
import openai
import streamlit as st
import pandas as pd
import mysql.connector
from mysql.connector import Error


def fetch_table_schema(cursor, table_name):
    """
    Fetches the schema (column names and types) of a table from the database.
    """
    cursor.execute(f"DESCRIBE {table_name}")
    schema = cursor.fetchall()
    column_names = [col[0] for col in schema]
    return column_names

import requests

from transformers import pipeline, LlamaForCausalLM, LlamaTokenizer

def generate_sql_query(user_prompt, column_names):
    """
    Generates an SQL SELECT query based on the user prompt and available column names.
    """
    try:
        # Format the column names as a string for the local model
        columns_description = ", ".join(column_names)
        schema_info = f"The table 'utilisation' has the following columns: {columns_description}."

        # Prompt for the local model
        system_message = (
            "You are an expert SQL generator. "
            "You should only generate code that is supported in MySQL. "
            "Create only SQL SELECT queries based on the given description. "
            "The table always uses the name 'utilisation'. "
            "Only use the column names provided in the schema. "
            "Do not insert the SQL query as commented code. "
            "When the word 'type' is mentioned, always consider it as projecttype. "
        )
        prompt = f"{system_message}\n\n{schema_info}\n\n{user_prompt}"

        # Load the LLaMA 3.1 model and tokenizer
        model_name = "path/to/your/local/llama3.1"  # Replace with the path to your local LLaMA 3.1 model
        tokenizer = LlamaTokenizer.from_pretrained(model_name)
        model = LlamaForCausalLM.from_pretrained(model_name)

        # Create a pipeline for text generation
        generator = pipeline('text-generation', model=model, tokenizer=tokenizer)

        # Generate the SQL query
        response = generator(prompt, max_length=200, num_return_sequences=1)
        sql_query = response[0]['generated_text'].strip()
        return sql_query
    except Exception as e:
        return f"Error generating SQL query: {str(e)}"

# Example usage
column_names = ["id", "name", "projecttype", "start_date", "end_date"]
user_prompt = "Generate a query to select all columns where the projecttype is 'Research'."
print(generate_sql_query(user_prompt, column_names))
