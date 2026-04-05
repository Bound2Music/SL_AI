
import streamlit as st
from sqlalchemy.engine import create_engine
import pandas as pd
from sqlalchemy.engine.url import URL
from dotenv import load_dotenv
import json
from openai import OpenAI
import os
import matplotlib.pyplot as plt



load_dotenv()

@st.cache
def convert_df(df):
    return 

# Set Environment Variables
drivername1 = os.environ.get('DRIVER_NAME')
username1 = os.environ.get('USER_NAME')
password1 = os.environ.get('PASSWORD')
host1 = os.environ.get('HOST')
database1 = os.environ.get('DATABASE')
query1 = os.environ.get('QUERY_DRIVER')

# Database connection URL
url = URL.create(
    drivername= drivername1,
    username= username1,
    password= password1,
    host= host1,  # e.g., "localhost" or a remote server address
    # port="1433",  # Default port for SQL Server
    database= database1,
     query={"driver": "ODBC Driver 17 for SQL Server"}

     # "Encrypt": "yes",
      #      "TrustServerCertificate": "no",
       #     "Connection Timeout": "30"
    # query=dict({"driver": "ODBC Driver 17 for SQL Server"})  # Specify the ODBC driver
)
# database_url = "mssql+pyodbc://azuresa:@c0d1ng99!@azuretestsvr.database.windows.net/projectdb?driver=ODBC+Driver+17+for+SQL+Server"


# Create the SQLAlchemy engine
engine = create_engine(url)


def getData():
    st.write("Enter your query")
    prompt = st.text_input("Enter")
    return prompt




def gpt():

    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY")
    )
    #completion = client.chat.completions.create(
    #completion = openai.ChatCompletion.create(
    completion = client.chat.completions.create(
        #model="text-davinci-003",
        model="gpt-3.5-turbo",
        #   messages=[
        #     {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
        #     {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
        #   ]
        messages=[{"role": "system",
                    "content":
                    """You are an AI assistant that is able to convert natural language into a properly formatted SQL query. The tables you will be querying is from the projectdb database.
                    Here is the schema of the table: {schema}
                    
                    You must always output your answer in JSON format with the following key-value pairs:
                    - "query": the SQL query that you generated 
                    - "error": an error message if the query is invalid, or null if the query is valid
                        """
                        } ,
                    {"role":"user",
                    "content":prompt #"show me only the product from the products table"
                        }
                    ],
        #prompt=user_input,
        #prompt = getData(),

        max_tokens = 500

    )
    index = completion.choices[0].message.content
    json_response = json.loads(index)
    sqlQuery = json_response['query']
    #print(sqlQuery)
    return sqlQuery


# Streamlit app
# def main():
st.title("SQL Server Natural Language Data Viewer")

try:
        with engine.connect() as connection:
            # query = "SELECT * FROM PRODUCTS"  # Replace 'PRODUCTS' with your actual table name if different
            tables = "SELECT TABLE_NAME FROM javafx.INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'"
            tablelist = pd.read_sql(tables, connection)
            # st.bar_chart(df, x="Product", y="Uom", color="Product")
           
            
except Exception as e:
    st.error(f"An error occurred: {e}")

prompt = getData()
# sqlQuery = gpt()


def ask():
    if prompt:

    # Connect to the database and read data
        try:
            with engine.connect() as connection:
                # query = "SELECT * FROM PRODUCTS"  # Replace 'PRODUCTS' with your actual table name if different
                query = gpt()  # Replace 'PRODUCTS' with your actual table name if different
                df = pd.read_sql(query, connection)
                st.write(df)
                st.bar_chart(df, x="Product", y="Uom", color="Product")
            
                
        except Exception as e:
            st.error(f"An error occurred: {e}")

        st.divider()

        @st.cache_data
        def convert_df(df):
            # IMPORTANT: Cache the conversion to prevent computation on every rerun
            return df.to_csv().encode('utf-8')

        csv = convert_df(df)

        st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='carData.csv',
        mime='text/csv',   
        )


ask2 = ask()
# tableList = []
# for row  in tablelist:
#     for columns in tablelist:
#         tableList += [tablelist.get(columns)] 

# tempList = ["hello", "testing", "now"]


# print(tableList[1:2])

st.sidebar.text_input("Name", "Enter Name")
st.sidebar.text_input("Password", "Enter Password")
st.sidebar.divider()
# st.sidebar.text_area("Tables", tableList[0:3])
st.sidebar.text_area("Tables", "PRODUCTS \n SHIPADDR \n BILLADDR")


# CSVData = main()
# prompt = getData()

# if __name__ == "__main__":
#     main()

#Open AI Environment
#openai-env\Scripts\activate
