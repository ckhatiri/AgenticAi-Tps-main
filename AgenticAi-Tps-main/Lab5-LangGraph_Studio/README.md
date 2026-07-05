# LAB 5 : LangGraph Studio & Multi-Agents

**Master BDCC — SMA et IAD | Prof. RETAL SARA**

## But du TP

Ce dossier reunit deux TP qui se completent, tous deux bases sur LangGraph Studio :

1. **Visualiser, tester et deboguer un agent** grace a LangGraph Studio — afficher le graphe de l'agent, l'executer pas a pas, et examiner les entrees/sorties de chaque node ;
2. **Construire un systeme multi-agents hierarchique** — un agent principal qui repartit des sous-taches vers des sous-agents specialises, ces derniers etant exposes comme de simples outils, le tout observable dans Studio.

---

## Organisation du projet

```
Lab5-LangGraph_Studio/
├── agent_simple.py      # TP "5 LangGraph Studio" : agent avec outil RAG simulé
├── multi_agents.py      # TP "8 Multi-Agents" : agent principal + 2 sous-agents
├── langgraph.json       # Configuration LangGraph Studio (3 graphes exposés)
├── pyproject.toml       # Dépendances uv
├── .env.example         # Template variables d'environnement
└── .gitignore
```

---

## Prerequis

- Python >= 3.10
- [uv](https://docs.astral.sh/uv/) installe
- [Ollama](https://ollama.com/) avec le modele `llama3.2:3b` (`ollama pull llama3.2:3b`)
- Un compte [LangSmith](https://smith.langchain.com/) muni d'une cle API

### Mise en place

```bash
# Dupliquer puis completer le fichier d'environnement
cp .env.example .env
# → Renseigner au moins : LANGSMITH_API_KEY

# Installer les dependances
uv sync
```

---

## Partie 1 — Creation d'un compte LangSmith et recuperation d'une cle

1. Se rendre sur **https://smith.langchain.com/**
2. Se connecter ou creer un compte (via Google, GitHub ou une adresse email)
3. Naviguer vers **Settings → API Keys → Create API Key**
4. Nommer la cle (par exemple `langgraph-project`) puis la copier
5. L'ajouter dans le fichier `.env` :
   ```
   LANGSMITH_API_KEY=lsv2_pt_...
   ```

---

## Partie 2 — Mise en place de l'agent

Le fichier `agent_simple.py` definit un agent LangChain dote d'un outil RAG simule :

```python
@tool
def rag_search_opt(query: str) -> str:
    """Recherche des informations dans le texte."""
    return "Le personnage principal est un jeune homme nommé Jack..."

agent = create_agent(
    model=ChatOllama(model="llama3.2:3b", temperature=0),
    tools=[rag_search_opt],
    system_prompt="Tu es un assistant spécialisé dans l'analyse de texte..."
)
```

**Verification rapide :**
```bash
uv run --active python -c "
from langchain.messages import HumanMessage
from agent_simple import agent
r = agent.invoke({'messages': [HumanMessage(content='Qui est le personnage principal ?')]})
print(r['messages'][-1].content)
"
```

---

## Partie 2 — Le fichier de configuration `langgraph.json`

Ce fichier indique a LangGraph Studio ou se trouve l'agent, quel environnement charger, et comment demarrer le projet :

```json
{
    "graphs": {
        "agent_simple": "./agent_simple.py:agent"
    },
    "env": "./.env",
    "source": {
        "kind": "uv",
        "root": "."
    }
}
```

| Cle | Role |
|---|---|
| `graphs` | Associe un nom de graphe a l'emplacement de la variable correspondante |
| `env` | Indique le fichier `.env` a charger |
| `source.kind` | Precise le gestionnaire de paquets utilise (`uv`) |
| `source.root` | Definit le repertoire racine du projet |

---

## Partie 2 — Demarrage de LangGraph Studio

```bash
uv run --active langgraph dev
```

Le serveur se lance sur **http://127.0.0.1:2024** et ouvre automatiquement l'interface Studio dans le navigateur, via **https://smith.langchain.com/studio**.

### Fonctionnalites disponibles dans Studio

| Fonctionnalite | Role |
|---|---|
| **Graph** | Affiche le graphe complet : `__start__ → model ⇄ tools → __end__` |
| **Chat** | Permet d'envoyer des messages et de voir les reponses en direct |
| **Interrupts** | Suspend l'execution a un node donne pour en inspecter l'etat |
| **Memory** | Montre l'etat persistant conserve pour le thread |
| **Tracing** | Detaille chaque appel au LLM ainsi que chaque appel d'outil |

### Graphe de l'agent

```
        __start__
            │
            ▼
          model  ◄────┐
            │         │
     ┌──────┴──────┐  │
     │             │  │
   __end__       tools─┘
```

---

## Ce qu'on observe

Une fois `langgraph dev` lance, l'interface Studio presente :

- Le graphe de l'agent avec ses nodes `model` et `tools`
- Un panneau **Input** permettant d'envoyer des messages
- La trace detaillee de chaque execution (appel LLM → appel d'outil → reponse)

**Exemple d'echange :**
> **User:** Qui est le personnage principal ?
> **Agent:** *(appelle `rag_search_opt`)* → Le personnage principal est Jack, un jeune homme qui découvre un ancien artefact magique.

---

# TP : Multi-Agents avec LangChain (`multi_agents.py`)

## Organisation hierarchique

```
                         main_agent
                  (call_subagent_1 / call_subagent_2)
                    │                         │
                    ▼                         ▼
              call_subagent_1           call_subagent_2
                    │                         │
                    ▼                         ▼
               subagent_1                subagent_2
              tools=[square_root]       tools=[square]
```

Chaque sous-agent est lui-meme un agent LangChain complet et independant, dispose de son propre LLM et de son propre outil, mais il est presente au `main_agent` comme un simple `@tool`. C'est le `main_agent` qui decide, selon la question posee, du sous-agent a solliciter.

## Partie 1 — Definition des outils

```python
@tool
def square_root(x: float) -> float:
    """Calculate the square root of a number"""
    return x ** 0.5

@tool
def square(x: float) -> float:
    """Calculate the square of a number"""
    return x ** 2
```

## Partie 2 — Mise en place des sous-agents

```python
subagent_1 = create_agent(model=model, tools=[square_root])
subagent_2 = create_agent(model=model, tools=[square])
```

## Partie 3 — Construction de l'agent principal

Chaque sous-agent est encapsule dans un `@tool` qui l'appelle et transmet sa reponse :

```python
@tool
def call_subagent_1(x: float) -> str:
    """Call subagent 1 in order to calculate the square root of a number"""
    response = subagent_1.invoke({"messages": [HumanMessage(content=f"Calculate the square root of {x}")]})
    return response["messages"][-1].content

main_agent = create_agent(
    model=model,
    tools=[call_subagent_1, call_subagent_2],
    system_prompt="You are a helpful assistant who can call subagents to "
                  "calculate the square root or square of a number.",
)
```

## Partie 4 — Appel des agents et affichage du resultat

```bash
uv run --active python multi_agents.py
```

### Resultats observes

```
Q: What is the square root of 456?
R: The square root of 456 is approximately 21.3542.

Q: What is the square of 12?
R: Thank you for the call! I've got the result. The square of 12 is indeed 144.
```

**Observation :** pour la premiere question, le `main_agent` sollicite `call_subagent_1`, qui fait appel a `subagent_1` (equipe de `square_root`) ; pour la seconde, il se tourne vers `call_subagent_2` / `subagent_2` (equipe de `square`). Le `main_agent` n'effectue jamais lui-meme le calcul — il **delegue** systematiquement aux sous-agents specialises et reformule ensuite leur reponse.

## Partie 5 — Visualisation des 3 agents dans LangGraph Studio

Le fichier `langgraph.json` expose les 3 graphes (`main_agent`, `subagent_1`, `subagent_2`) :

```json
{
    "graphs": {
        "agent_simple": "./agent_simple.py:agent",
        "main_agent": "./multi_agents.py:main_agent",
        "subagent_1": "./multi_agents.py:subagent_1",
        "subagent_2": "./multi_agents.py:subagent_2"
    },
    "env": "./.env",
    "source": { "kind": "uv", "root": "." }
}
```

```bash
uv run --active langgraph dev
```

Dans Studio, le selecteur de graphe (situe en haut) permet de passer d'un graphe a l'autre — `agent_simple`, `main_agent`, `subagent_1`, `subagent_2` — d'observer chacun d'eux (`__start__ → model ⇄ tools → __end__`) et de suivre pas a pas la trace d'une delegation : `main_agent → tools (call_subagent_1) → réponse`.