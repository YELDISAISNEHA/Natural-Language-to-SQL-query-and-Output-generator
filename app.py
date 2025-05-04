import os
import pandas as pd
import mysql.connector
from langchain_ollama import ChatOllama
import streamlit as st
import tempfile

# Connect to MySQL
@st.cache_resource
def connect_mysql():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="RGUKT123",
            database="major_project"
        )
    except Exception as e:
        st.error(f"Error connecting to MySQL: {e}")
        return None

# Load CSV to MySQL
def load_csv_to_mysql(file, mydb):
    try:
        df = pd.read_csv(file)
        cursor = mydb.cursor()
        table_name = "csv_data"

        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        columns = [f"`{col}` TEXT" for col in df.columns]
        create_table = f"CREATE TABLE {table_name} ({', '.join(columns)})"
        cursor.execute(create_table)

        cols = ", ".join(f"`{col}`" for col in df.columns)
        placeholders = ", ".join(["%s"] * len(df.columns))
        insert_query = f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders})"

        for _, row in df.iterrows():
            cursor.execute(insert_query, [str(val) for val in row.tolist()])

        mydb.commit()
        st.success("CSV data loaded into MySQL successfully.")
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
        if mydb.is_connected():
            mydb.rollback()

# Generate MySQL Query
def generate_query(user_input, mydb):
    try:
        cursor = mydb.cursor()
        cursor.execute("DESCRIBE csv_data")
        field_names = [col[0] for col in cursor.fetchall()]
        llm = ChatOllama(model="mistral")

        prompt = f"""
You are a MySQL expert. Only respond with a MySQL SELECT query in this exact format:
SELECT column1, column2 FROM csv_data WHERE condition;

Rules:
- Use only these fields from the 'csv_data' table: {field_names}
- All field names are case-sensitive.
- String values must be in single quotes.
- For GROUP BY queries, do not include non-aggregated columns in SELECT unless they are also in GROUP BY.
- If extracting year from a date column (e.g., LaunchDate), use the YEAR() function in MySQL.
- Assume all dates are stored as TEXT in the format 'YYYY-MM-DD'.

User request:
\"{user_input}\"
"""

        response = llm.invoke(prompt)
        query = response.content.strip()
        return query if query.lower().startswith("select") else None
    except Exception as e:
        st.error(f"Error generating query: {e}")
        return None

# Execute the query
def execute_query(query, mydb):
    try:
        cursor = mydb.cursor(dictionary=True)
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        st.error(f"Query execution error: {e}")
        return []

# Streamlit App
def main():
    st.title("Natural Language to SQL Query and Output Generator")
    mydb = connect_mysql()
    if not mydb:
        st.stop()

    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
    if uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name
        load_csv_to_mysql(tmp_path, mydb)

    st.markdown("---")
    user_input = st.text_input("Ask your query (in plain English):")
    if user_input:
        query = generate_query(user_input, mydb)
        if query:
            st.code(query, language="sql")
            data = execute_query(query, mydb)
            if data:
                df = pd.DataFrame(data)
                st.dataframe(df)

                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button("Download Result as CSV", csv, "result.csv", "text/csv")
            else:
                st.warning("No matching records found.")
        else:
            st.error("Could not generate a valid SQL query.")

if __name__ == "__main__":
    main()
