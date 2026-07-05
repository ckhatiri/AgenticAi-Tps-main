# TP : Agent Chef Cuisinier Personnel

**Master BDCC — SMA et IAD | Prof. RETAL SARA**

## But du TP

Concevoir un agent intelligent tenant le role d'un chef cuisinier personnel, capable de :
- Recuperer la liste des ingredients dont dispose l'utilisateur
- Retenir ses preferences et ses restrictions alimentaires
- S'appuyer sur une base de recettes locale (RAG) pour proposer des plats adaptes
- Enrichir ses reponses grace a une recherche web (Tavily, facultative)

---

## Organisation du projet

```
TP-Chef_personnel/
├── chef_agent.py    # Agent principal avec tous les outils
├── recipes.txt      # Base de recettes locale (15 recettes)
├── pyproject.toml
├── .env.example
└── .gitignore
```

---

## Prerequis

- Python >= 3.10 · [uv](https://docs.astral.sh/uv/) · [Ollama](https://ollama.com/) avec `llama3.2:3b`
- (Facultatif) une cle API Tavily pour activer la recherche web

```bash
uv sync
cp .env.example .env   # Renseigner TAVILY_API_KEY si disponible
```

---

## Fonctionnement general

```
Utilisateur
    |
    v
chef_agent (llama3.2:3b)
    |         |          |            |
    v         v          v            v
search_     search_   remember_   get_
recipes_    web()     preference  preferences
rag()       (Tavily)  (Command)   (ToolRuntime)
    |                     |            |
    v                     v            v
InMemory              ChefState     ChefState
VectorStore           .preferences  .preferences
(recipes.txt)         (update)      (read)
    |
    v
HuggingFace
Embeddings
(all-MiniLM-L6-v2)
```

---

## Les composants du systeme

### RAG — La base de recettes

Le fichier `recipes.txt` regroupe 15 recettes detaillees (pates, risotto, omelette, curry, ratatouille...), decoupees en morceaux puis indexees grace a des embeddings semantiques :

```python
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = InMemoryVectorStore.from_documents(chunks, embeddings)
```

### La memoire — un etat persiste

Les preferences de l'utilisateur sont conservees dans un `ChefState` sur mesure, rendu persistant grace a `InMemorySaver` :

```python
class ChefState(AgentState):
    preferences: list[str]
```

L'outil `remember_preference` actualise cet etat via `Command` :

```python
@tool
def remember_preference(preference: str, runtime: ToolRuntime) -> Command:
    """Store a user preference in long-term memory."""
    current = runtime.state.get("preferences", [])
    return Command(update={
        "preferences": current + [preference],
        "messages": [ToolMessage("Preference saved...", tool_call_id=runtime.tool_call_id)]
    })
```

### Les outils mis a disposition

| Outil | Role |
|---|---|
| `search_recipes_rag` | Effectue une recherche semantique dans la base de recettes locale |
| `search_web` | Lance une recherche web via Tavily (necessite `TAVILY_API_KEY`) |
| `remember_preference` | Enregistre une preference ou une allergie dans l'etat |
| `get_preferences` | Recupere l'ensemble des preferences deja memorisees |

---

## Lancement

```bash
uv run --active python chef_agent.py
```

---

## Resultats observes

```
User  : Je suis vegetarien et j'adore la cuisine italienne.
Chef  : Bonjour ! Voici trois recettes qui correspondent à vos préférences :
        1. Pasta au Pomodoro — tomates, basilic, ail, huile d'olive
        2. Ratatouille — légumes du soleil cuits à feu doux
        3. Pâtes au Pesto — basilic frais, parmesan, pignons de pin

User  : Je suis allergique aux arachides.
Chef  : Désolé de vous apprendre cela ! Voici des alternatives sans arachides :
        1. Pasta au Pomodoro
        2. Ratatouille
        3. Pâtes au Spinaci (épinards + tomates)

User  : J'ai : des pates, des tomates, de l'ail, de l'huile d'olive, du basilic et du parmesan.
Chef  : Vous pouvez préparer :
        - Pasta al Pomodoro : faire sauter l'ail, ajouter tomates, mélanger aux pâtes, garnir de basilic
        - Pâtes au Basilic : sauce basilic-ail-huile d'olive rapide en 15 minutes

User  : Et si j'ajoute des oeufs et des epinards ?
Chef  : Avec ces ajouts :
        - Pasta al Pomodoro enrichie : ajouter épinards et oeufs battus en fin de cuisson
        - Pâtes complètes : mélanger pâtes, sauce basilic, oeufs, épinards frais
```

---

## Prompt systeme utilise

```python
SYSTEM_PROMPT = """You are a personal chef assistant. Your role is to help users discover
delicious dishes they can prepare with their available ingredients.

You have access to:
- search_recipes_rag: search your local recipe knowledge base
- search_web: search the internet for additional recipes and techniques
- remember_preference: store user preferences, allergies, and dietary restrictions
- get_preferences: retrieve the user's stored preferences

When a user tells you their available ingredients:
1. First check their preferences with get_preferences
2. Search the recipe knowledge base with search_recipes_rag
3. Suggest 2-3 concrete dishes adapted to ingredients and preferences
4. Always respect dietary restrictions and allergies"""
```