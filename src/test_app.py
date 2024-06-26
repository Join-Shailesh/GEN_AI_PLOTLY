from Langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import Humankessage
from Langchain_groq import ChatGroq
from dash import Dash, html, dcc, callback, Output, Input, State
import dash_ag_grid as dag
import pandas as pd
import re

from dotenv import find_dotenv, load_dotenv
import os

#Load the api key
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
GROQ_API_KEY= os.getenv("GROQ_API_KEY") # Create a .env file and write: GROQ_API_KEY="insert-your-groq-api-key

#Load the dataset, grab the first 5 rows, and convert to string so that the LLM can read the data
df = pd.read_csv('space-mission-data.csv')
df_5_rows =  df.head() 
csv_string= df_5_rows.to_string(index=False)
 

#choose the model
model = ChatGroq(
    api_key=GROQ_API_KEY,
    model="llama3-70b-8192",
    #model="Mixtral-8x7b-32768",
)
 
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "systas",
            "You're a data visualization expert and use your favourite graphing Library Flotly only. Suppose, that "
            "the data is provided as a space-alision-data.csv file. Here are the first 5 rows of the data set: (data) "
            "Follow the user's indications when creating the graph." 
        ),
        MessagesPlaceholder(variable_name="messsages"),
    ]
)

chain = prompt | model

