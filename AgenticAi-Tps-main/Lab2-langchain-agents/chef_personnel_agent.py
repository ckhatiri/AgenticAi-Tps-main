"""
TP LangChain - Agent culinaire personnel

Capacités implémentées :
- message système personnalisé
- mémoire conversationnelle via InMemorySaver
- outil de recherche web (Tavily)
- suggestion de plats adaptés aux ingrédients et préférences de l'utilisateur
"""

import os
from typing import Any, Dict

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain.tools import tool
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import InMemorySaver
from tavily import TavilyClient


load_dotenv()


def build_web_search_tool():
    """Crée l'outil de recherche Tavily avec un message d'erreur explicite si la clé API est absente."""
    api_key = os.getenv("TAVILY_API_KEY")

    if not api_key:
        @tool("web_search")
        def web_search(query: str) -> Dict[str, Any]:
            """
            Recherche web non disponible : TAVILY_API_KEY manquante dans la configuration.

            Args:
                query: terme ou question de recherche culinaire
            """
            return {
                "status": "error",
                "message": (
                    "La recherche web est indisponible. "
                    "Ajoutez TAVILY_API_KEY dans le fichier .env."
                ),
                "query": query,
            }

        return web_search

    tavily_client = TavilyClient(api_key=api_key)

    @tool("web_search")
    def web_search(query: str) -> Dict[str, Any]:
        """
        Interroge le web pour obtenir des informations culinaires.

        Args:
            query: question portant sur une recette, une technique ou un ingrédient
        """
        return tavily_client.search(query, max_results=3)

    return web_search


def build_agent():
    """Instancie le modèle de langage, l'outil de recherche web et la mémoire conversationnelle."""
    model_name = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
    temperature = float(os.getenv("OLLAMA_TEMPERATURE", "0"))

    model = ChatOllama(
        model=model_name,
        temperature=temperature,
    )

    system_prompt = """
Tu es un assistant culinaire personnel attentionné.

Tes missions :
- accompagner l'utilisateur dans la préparation de repas à partir des ingrédients disponibles
- mémoriser ses préférences, ses allergies, son régime et ses contraintes de temps
- consulter web_search uniquement lorsqu'une information culinaire précise ou récente est indispensable
- suggérer des plats concrets, accessibles et adaptés à la situation

Comment répondre :
- toujours en français
- en tenant compte de l'ensemble de la conversation
- si un élément manque, formule une hypothèse explicite
- privilégie les recettes rapides, réalisables en moins de 30 minutes avec peu d'ingrédients
- ne suppose jamais la disponibilité d'un ingrédient non mentionné par l'utilisateur
- signale clairement les ingrédients optionnels
- sois concis, sans introduction répétitive
- ne fais appel à web_search que si c'est vraiment nécessaire
- organise ta réponse ainsi :
  1. Plat suggéré
  2. Pourquoi ce choix convient
  3. Ingrédients utilisés
  4. Étapes de préparation
  5. Variante ou astuce
"""

    agent = create_agent(
        model=model,
        tools=[build_web_search_tool()],
        system_prompt=system_prompt,
        checkpointer=InMemorySaver(),
    )

    return agent


def ask_agent(agent, user_text: str, thread_id: str = "chef-thread-1") -> str:
    """Transmet un message à l'agent en conservant l'historique de la session."""
    response = agent.invoke(
        {"messages": [HumanMessage(content=user_text)]},
        {"configurable": {"thread_id": thread_id}},
    )
    return response["messages"][-1].content


def run_demo():
    """Scénario de démonstration pour valider le TP."""
    agent = build_agent()

    prompts = [
        "Bonjour, je suis Lina. Je ne supporte pas le piment et je suis végétarienne.",
        "Note également que je dispose de 30 minutes maximum pour cuisiner chaque soir.",
        "J'ai dans mon réfrigérateur des œufs, des tomates, du fromage, des oignons et du pain complet. Suggère-moi un ou deux plats qui correspondent à mes ingrédients et mes préférences.",
        (
            "Propose-moi une alternative différente. "
            "Si besoin, consulte le web pour vérifier une idée de recette."
        ),
    ]

    for index, prompt in enumerate(prompts, start=1):
        print(f"\n--- Question {index} ---")
        print(f"Utilisateur: {prompt}\n")
        answer = ask_agent(agent, prompt)
        print("Agent:")
        print(answer)


def run_interactive():
    """Mode interactif pour la démonstration en séance."""
    agent = build_agent()
    thread_id = "chef-thread-1"

    print("Assistant culinaire personnel prêt.")
    print("Saisissez 'quit' pour terminer la session.\n")

    while True:
        user_text = input("Vous: ").strip()
        if user_text.lower() in {"quit", "exit"}:
            print("Fin de session.")
            break
        if not user_text:
            continue

        answer = ask_agent(agent, user_text, thread_id=thread_id)
        print(f"\nChef: {answer}\n")


if __name__ == "__main__":
    mode = os.getenv("APP_MODE", "interactive").lower()
    if mode == "interactive":
        run_interactive()
    else:
        run_demo()
