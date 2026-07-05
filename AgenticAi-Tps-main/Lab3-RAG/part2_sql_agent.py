from langchain_community.utilities import SQLDatabase
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent

# --- Établissement de la connexion à la base SQLite ---
db = SQLDatabase.from_uri("sqlite:///Chinook.db")

# --- Définition de l'outil d'interrogation SQL ---
@tool
def sql_query(query: str) -> str:
    """Obtain information from the database using SQL queries"""
    try:
        print(f"Executing SQL query: {query}")
        return db.run(query)
    except Exception as e:
        return f"Error: {e}"

# Test direct de l'outil SQL
print("--- Test du tool sql_query ---")
print(sql_query.invoke("SELECT * FROM Artist LIMIT 10"))

# --- Initialisation de l'agent SQL ---
model = ChatOllama(
    model="llama3.2:3b",
)

system_prompt = """You are a database specialist with expertise in SQL.

Guidelines:
- Always rely on the sql_query tool to retrieve data
- The sql_query tool accepts a SQL query string and returns the query result
- Only reference columns that exist in the schema
- If the requested information is not available, clearly say so
- Never guess or fabricate data
- Format the output in a clear, human-readable way — never return raw SQL or raw query results

Database schema:
Table Artist:
- ArtistId
- Name
"""

agent = create_react_agent(
    model=model,
    tools=[sql_query],
    prompt=system_prompt
)

# --- Interrogation de la base en langage naturel ---
question = HumanMessage(content="Give me the first 5 artists in the database")
response = agent.invoke(
    {"messages": [question]}
)
print("\n--- Réponse de l'Agent SQL ---")
print(response["messages"][-1].content)
