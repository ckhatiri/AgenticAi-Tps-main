# LAB 6 : Contexte et Etat dans un agent

**Master BDCC — SMA et IAD | Prof. RETAL SARA**

## But du TP

Saisir puis mettre en application la distinction entre **contexte** (donnees fixes transmises au moment de l'invocation) et **etat** (donnees modifiables qui evoluent et se conservent au fil de la conversation) au sein d'un agent LangChain/LangGraph.

---

## Organisation du projet

```
Lab6-Contexte_et_Etat/
├── agent_context.py   # Partie 1 : le contexte (immuable, par invocation)
├── agent_state.py     # Partie 2 : l'état (mutable, persisté par thread)
├── pyproject.toml
├── .env.example
└── .gitignore
```

---

## Prerequis

- Python >= 3.10 · [uv](https://docs.astral.sh/uv/) · [Ollama](https://ollama.com/) avec `llama3.2:3b`

```bash
uv sync
```

---

## Principe : Contexte contre Etat

```
CONTEXTE                              ÉTAT
────────────────────                  ────────────────────
Immuable pendant l'invocation         Mutable pendant la conversation
Fourni via invoke(context=...)        Modifié par les tools via Command
Pas persisté entre les appels         Persisté par thread_id (checkpointer)
Ex : profil utilisateur, paramètres   Ex : préférences révélées au fil du chat
```

---

## Partie 1 — Le contexte (`agent_context.py`)

Le contexte correspond a des informations deja connues **avant** que la conversation ne debute (par exemple le profil du lecteur d'une bibliotheque : nom, niveau d'abonnement, langue preferee). Il est declare via `context_schema` et transmis a chaque appel grace a `invoke(..., context=...)`.

```python
@dataclass
class ReaderProfile:
    name: str = "Khalid"
    membership: str = "standard"
    preferred_language: str = "français"

@tool
def get_membership_level(runtime: ToolRuntime) -> str:
    """Get the library membership level of the current reader."""
    return runtime.context.membership

agent_with_context = create_agent(
    model=model,
    tools=[get_membership_level, get_preferred_language],
    context_schema=ReaderProfile,
)

response = agent_with_context.invoke(
    {"messages": [HumanMessage(content="Quel est mon niveau d'abonnement ?")]},
    context=ReaderProfile(),
)
```

### Lancement

```bash
uv run --active python agent_context.py
```

### Resultats observes

```
--- Partie 2 : Agent sans accès au contexte ---
Je ne suis pas en mesure de vous fournir des informations sur votre compte
d'abonnement à une bibliothèque spécifique. [...] Contactez la bibliothèque
directement [...]

--- Partie 3 : Agent avec accès au contexte ---
Votre niveau d'abonnement à la bibliothèque est standard.

--- Partie 4 : Changement de contexte (lecteur premium) ---
Votre niveau d'abonnement à la bibliothèque est de niveau "premium".
```

**Ce qu'on en retient :** en l'absence d'un tool permettant de lire `runtime.context`, le LLM n'a aucun moyen d'acceder au contexte (Partie 2). Des qu'un tool dedie est fourni, l'acces devient direct (Partie 3). Le contexte, lui, peut varier librement entre deux appels — chaque `invoke` peut ainsi representer un lecteur different (Partie 4).

---

## Partie 2 — L'etat (`agent_state.py`)

L'etat correspond a des informations **decouvertes en cours de** conversation, qui doivent rester accessibles d'un echange a l'autre (par exemple le genre litteraire prefere du lecteur, mentionne au fil de la discussion). Cela passe par une extension d'`AgentState`, modifiee par un tool via `Command(update=...)`.

```python
class LibraryState(AgentState):
    favourite_genre: str

@tool
def remember_favourite_genre(genre: str, runtime: ToolRuntime) -> Command:
    """Store the reader's favourite literary genre once they reveal it."""
    return Command(update={
        "favourite_genre": genre,
        "messages": [ToolMessage(f"Genre favori enregistré : {genre}",
                                 tool_call_id=runtime.tool_call_id)]
    })

@tool
def recall_favourite_genre(runtime: ToolRuntime) -> str:
    """Read the reader's favourite literary genre from the persisted state."""
    try:
        return runtime.state["favourite_genre"]
    except KeyError:
        return "Aucun genre favori enregistré pour le moment."

agent = create_agent(
    model=model,
    tools=[remember_favourite_genre, recall_favourite_genre],
    state_schema=LibraryState,
    checkpointer=InMemorySaver(),
)
```

### Lancement

```bash
uv run --active python agent_state.py
```

### Resultats observes

```
--- Partie 6 : enregistrer le genre favori ---
Vous aimez les romans de science-fiction ! [...] je peux vous suggérer
quelques titres populaires du genre [...]
État courant : science-fiction

--- Partie 6 (suite) : récupérer le genre persisté ---
Votre genre littéraire favori est bien la science-fiction ! [...]

--- Partie 7 : nouveau thread, état vide ---
Je suis désolé, mais je n'ai pas d'informations sur vos préférences
littéraires. Si vous voulez partager votre genre favori avec moi [...]
```

**Ce qu'on en retient :** au sein d'un meme `thread_id` (`reader-1`), l'agent retient le genre favori entre plusieurs tours grace au `checkpointer` (Partie 6). En revanche, avec un nouveau `thread_id` (`reader-2`), l'etat repart entierement de zero — la persistance reste donc cloisonnee par thread (Partie 7).

---

## Tableau comparatif

| | Contexte (`agent_context.py`) | Etat (`agent_state.py`) |
|---|---|---|
| **Mutabilite** | Fixe pendant toute l'invocation | Modifiable, via les tools |
| **Provenance** | Transmis par l'appelant (`context=`) | Elabore au cours de la conversation |
| **Persistance** | Absente — redefini a chaque appel | Conserve par `thread_id` grace au `checkpointer` |
| **Mode de lecture** | `runtime.context` | `runtime.state[...]` |
| **Mode d'ecriture** | — (non modifiable) | `Command(update={...})` |
| **Usage typique** | Profil utilisateur, parametres de session | Preferences exprimees, memoire de la conversation |