from dataclasses import dataclass

from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain.tools import ToolRuntime, tool
from langchain_ollama import ChatOllama

# ============================================================
# PARTIE 1 : Contexte — données immuables fournies à l'invocation
# ============================================================
# Le contexte regroupe les données disponibles AVANT le début de la conversation
# (profil lecteur, paramètres de session...). Ces données sont fournies une seule fois
# via `context=` et demeurent inchangées tout au long de l'invocation.


@dataclass
class ReaderProfile:
    name: str = "Lina"
    membership: str = "standard"
    preferred_language: str = "français"


model = ChatOllama(model="llama3.2:3b", temperature=0)

# ============================================================
# PARTIE 2 : Agent sans accès au contexte
# ============================================================
# Bien que `context_schema` soit déclaré, l'agent ne dispose d'aucun outil
# pour accéder au contexte : le LLM est donc incapable de l'exploiter.

agent_no_access = create_agent(model=model, context_schema=ReaderProfile)

response = agent_no_access.invoke(
    {"messages": [HumanMessage(content="Quel est mon niveau d'abonnement à la bibliothèque ?")]},
    context=ReaderProfile(),
)
print("--- Partie 2 : Agent sans accès au contexte ---")
print(response["messages"][-1].content)


# ============================================================
# PARTIE 3 : Agent avec des tools qui lisent le contexte
# ============================================================
# `runtime.context` donne à un outil l'accès aux données du contexte actif —
# ici le profil du lecteur de la bibliothèque.


@tool
def get_membership_level(runtime: ToolRuntime) -> str:
    """Get the library membership level of the current reader."""
    return runtime.context.membership


@tool
def get_preferred_language(runtime: ToolRuntime) -> str:
    """Get the preferred reading language of the current reader."""
    return runtime.context.preferred_language


agent_with_context = create_agent(
    model=model,
    tools=[get_membership_level, get_preferred_language],
    context_schema=ReaderProfile,
)

response = agent_with_context.invoke(
    {"messages": [HumanMessage(content="Quel est mon niveau d'abonnement à la bibliothèque ?")]},
    context=ReaderProfile(),
)
print("\n--- Partie 3 : Agent avec accès au contexte ---")
print(response["messages"][-1].content)


# ============================================================
# PARTIE 4 : Changer le contexte d'une invocation à l'autre
# ============================================================
# Le contexte n'est pas persisté entre les appels : chaque invocation peut
# recevoir un contexte différent (autre lecteur, autre type d'abonnement).

response = agent_with_context.invoke(
    {"messages": [HumanMessage(content="Quel est mon niveau d'abonnement à la bibliothèque ?")]},
    context=ReaderProfile(name="Nadia", membership="premium", preferred_language="anglais"),
)
print("\n--- Partie 4 : Changement de contexte (lectrice premium) ---")
print(response["messages"][-1].content)
