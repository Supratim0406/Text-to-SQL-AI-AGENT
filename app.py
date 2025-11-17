import os
import sqlite3
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Generate SQL from natural language
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content([prompt, question])
    return response.text.strip()

# Execute SQL
def read_sql_query(db, sql):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    conn.close()
    return rows

# Prompt for LLM
prompt = """
You are an expert in converting English questions to SQL query!
The SQL database has the table name EMPLOYEES with columns: EMPLOYEE_ID, NAME, EMAIL, DEPARTMENT, POSITION, SALARY, JOIN_DATE.

IMPORTANT RULES:
1. Return ONLY the SQL query without any explanations
2. Do not use markdown code blocks (no ```sql or ```)
3. Use proper SQL syntax for SQLite
4. For text values, use single quotes: WHERE DEPARTMENT='HR'
5. For counting records, use: SELECT COUNT(*) FROM EMPLOYEES

Examples:
- Question: "How many employees are in IT department?"
  SQL: SELECT COUNT(*) FROM EMPLOYEES WHERE DEPARTMENT='HR'

- Question: "Show all employees"
  SQL: SELECT * FROM EMPLOYEES

- Question: "Find employees named John"
  SQL: SELECT * FROM EMPLOYEES WHERE NAME='John'

Now convert this question to SQL:
"""

# Streamlit App
st.set_page_config(page_title="I can Retrieve Any SQL query")
st.header("🚀 AI TEXT to SQL Assistant for your DB")

question=st.text_input("Enter your query here: ",key="input")
submit=st.button("Ask the question")

# if submit is clicked
if submit:
    with st.spinner('🔄 Generating SQL query and fetching results...'):
        sql_query=get_gemini_response(question,prompt)
        st.write("📌 Generated SQL:", sql_query)
        try:
            rows = read_sql_query("employees.db", sql_query)
            st.subheader("Results:")
            for row in rows:
                st.write(row)
        except Exception as e:
            st.error(f"SQL Error: {e}")
