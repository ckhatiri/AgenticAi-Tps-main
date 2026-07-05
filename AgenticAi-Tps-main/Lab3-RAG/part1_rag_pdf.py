from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent

# --- Chargement et lecture des pages du PDF ---
loader = PyPDFLoader("acmecorp-employee-handbook.pdf")
data = loader.load()
print(f"Pages chargées : {len(data)}")
print(data)

# --- Découpage du texte en blocs ---
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200, add_start_index=True
)
all_splits = text_splitter.split_documents(data)
print(f"\nNombre de chunks : {len(all_splits)}")

# --- Vectorisation des blocs via HuggingFace ---
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# --- Initialisation du vectorstore en mémoire ---
vector_store = InMemoryVectorStore(embeddings)

# --- Ajout des blocs au vectorstore ---
ids = vector_store.add_documents(documents=all_splits)
print(f"Documents indexés : {len(ids)}")

# --- Requête par similarité sémantique ---
results = vector_store.similarity_search(
    "How many days of vacation does an employee get in their first year?"
)
print("\n--- Résultat de la recherche sémantique ---")
print(results[0])

# --- Construction de l'agent RAG ---
@tool
def search_handbook(query: str) -> str:
    """Search the employee handbook for relevant information."""
    results = vector_store.similarity_search(query)
    return results[0].page_content

model = ChatOllama(
    model="llama3.2:3b",
    temperature=0
)

agent = create_react_agent(
    model=model,
    tools=[search_handbook],
    prompt="You are a helpful agent that can search the employee handbook for information."
)

response = agent.invoke(
    {"messages": [HumanMessage(content="How many days of vacation does an employee get in their first year?")]}
)
print("\n--- Réponse de l'Agent RAG ---")
print(response["messages"][-1].content)
