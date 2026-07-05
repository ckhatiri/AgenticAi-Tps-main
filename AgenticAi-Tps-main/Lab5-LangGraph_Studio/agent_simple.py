from langchain_ollama import ChatOllama
from langchain.messages import HumanMessage
from langchain.tools import tool
from langchain.agents import create_agent


@tool
def rag_search_opt(query: str) -> str:
    """Extrait les passages pertinents du corpus de texte."""
    results = (
        "La protagoniste est une jeune chercheuse prénommée Yasmine, "
        "qui met au point une intelligence artificielle dotée de conscience. "
        "Cette découverte la propulse au cœur d'enjeux internationaux, "
        "car des organisations cherchent à s'emparer de son invention. "
        "Yasmine devra protéger son projet tout en faisant face aux dilemmes éthiques qu'il soulève."
    )
    return results


llm = ChatOllama(
    model="llama3.2:3b",
    temperature=0
)

agent = create_agent(
    model=llm,
    tools=[rag_search_opt],
    system_prompt=(
        "Tu es un assistant dédié à l'analyse et à l'interprétation de textes narratifs. "
        "Appuie-toi sur l'outil rag_search_opt pour répondre aux questions à partir du corpus. "
        "Formule des réponses précises en citant explicitement les éléments du contexte."
    )
)
