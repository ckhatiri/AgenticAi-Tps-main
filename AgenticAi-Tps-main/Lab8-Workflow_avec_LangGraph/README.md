# LAB 8 : Workflows avec LangGraph

**Master BDCC — SMA et IAD | Prof. RETAL SARA**

## But du TP

Explorer les elements fondamentaux d'un **workflow LangGraph** : graphe d'etats, nodes, edges, reducers, etat de type message, branchements conditionnels et boucles.

---

## Organisation du projet

```
Lab8-Workflow_avec_LangGraph/
├── hello_graph.py                      # Partie 1 : premier graphe (StateGraph + MessagesState)
├── workflows/
│   └── two_step_workflow.py            # Partie 2 : workflow séquentiel à deux étapes
├── reducers_demo.py                    # Partie 3 : reducer (fusion de listes avec `add`)
├── message_state.py                    # Partie 4 : état de type message
├── conditional_workflow.py             # Partie 5 : branchement conditionnel
├── workflow_loop.py                    # Partie 6 : workflow en boucle + export PNG du graphe
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

## Principe : qu'est-ce qu'un Workflow LangGraph

```
StateGraph(State)
   │
   ├── add_node("nom", fonction)     # une étape du workflow
   ├── add_edge(START, "nom")        # liaison séquentielle
   ├── add_conditional_edges(...)    # branchement dynamique selon l'état
   │
   └── compile() ──► graph.invoke(state_initial)
```

Chaque node recoit l'etat en cours et renvoie un **dictionnaire de mise a jour** ; LangGraph integre ensuite ces changements dans l'etat global, en suivant soit un remplacement par defaut, soit un **reducer** personnalise.

---

## Partie 1 — Premier graphe (`hello_graph.py`)

Il s'agit du graphe le plus simple possible : un seul node, `hello`, qui ajoute un message de l'assistant.

```python
def hello_node(state: MessagesState):
    return {"messages": [{"role": "ai", "content": "Hello World"}]}

builder = StateGraph(MessagesState)
builder.add_node("hello", hello_node)
builder.add_edge(START, "hello")
builder.add_edge("hello", END)
```

```bash
uv run --active python hello_graph.py
```

**Resultat obtenu :**
```
Hello World
```

---

## Partie 2 — Workflow a deux etapes (`workflows/two_step_workflow.py`)

Le node `refine_topic` reformule le sujet, puis `write_joke` produit une blague a partir de ce sujet affine — l'execution suit un ordre strictement sequentiel (`START → refine_topic → write_joke → END`).

```bash
uv run --active python workflows/two_step_workflow.py
```

**Resultat obtenu :**
```
{'topic': 'ice cream (and cats)', 'joke': 'Here is a joke about ice cream (and cats).'}
```

---

## Partie 3 — Le reducer (`reducers_demo.py`)

Un **reducer** precise comment combiner une nouvelle valeur avec l'ancienne dans l'etat, plutot que de simplement l'ecraser. Ici, `log: Annotated[list[str], add]` fait que chaque valeur retournee par un node est **ajoutee** a la liste existante grace a `operator.add`.

```python
class State(TypedDict):
    topic: str
    log: Annotated[list[str], add]
```

```bash
uv run --active python reducers_demo.py
```

**Resultat obtenu :**
```
['step_a saw topic=langgraph', 'step_b finishing topic=langgraph', 'step_c finishing topic at last=langgraph']
```

Sans reducer, seule la derniere valeur de `log` serait conservee ; grace a `add`, l'historique complet des trois etapes est preserve.

---

## Partie 4 — Etat de type message (`message_state.py`)

Le champ `messages: Annotated[list[BaseMessage], add]` permet d'accumuler automatiquement l'historique de la conversation a chaque passage dans un node, sur le meme principe que `log` dans la partie precedente, mais applique cette fois aux messages.

```bash
uv run --active python message_state.py
```

**Resultat obtenu :**
```
[{'role': 'user', 'content': 'hello'},
 {'role': 'ai', 'content': 'Step 1: got your message.'},
 {'role': 'ai', 'content': 'Step 2: got your message 1.'}]
```

Le message initial de l'utilisateur reste present, et chaque node (`echo`, `echo_1`) vient ajouter son propre message a la suite — le compteur `steps` augmente d'une unite a chaque etape.

---

## Partie 5 — Workflow conditionnel (`conditional_workflow.py`)

Le node `check_joke` fait office de **routeur conditionnel** : si la blague generee contient deja un `"!"`, le graphe se termine immediatement ; sinon, il passe par le node `improve_joke`.

```python
def check_joke(state: State) -> Literal["improve", "end"]:
    if "!" in state["joke"]:
        return "end"
    return "improve"

builder.add_conditional_edges("generate_joke", check_joke,
                              {"improve": "improve_joke", "end": END})
```

```bash
uv run --active python conditional_workflow.py
```

**Resultat obtenu :**
```
{'topic': 'cats', 'joke': 'A joke about cats maybe ? ', 'improved': 'A joke about cats maybe ?  !!!'}
```

La blague generee initialement ne contient pas de `"!"` : le graphe est donc redirige vers `improve_joke`, qui ajoute `" !!!"` et remplit le champ `improved`.

---

## Partie 6 — Workflow en boucle (`workflow_loop.py`)

Le node `step` incremente la valeur `n` et consigne chaque iteration dans `log`. La fonction `should_continue` renvoie vers `step` tant que `n < 5`, puis met fin au graphe (`END`).

```python
def should_continue(state: State) -> Literal["again", "stop"]:
    return "again" if state["n"] < 5 else "stop"

builder.add_conditional_edges("step", should_continue, {"again": "step", "stop": END})
```

```bash
uv run --active python workflow_loop.py
```

**Resultat obtenu :**
```
{'n': 5, 'log': ['n is now 1', 'n is now 2', 'n is now 3', 'n is now 4', 'n is now 5']}
Graphe exporté dans graph2.png
```

Le graphe repasse cinq fois par `step` avant d'atteindre la condition d'arret, puis genere une representation visuelle du graphe (`graph2.png`) grace a `draw_mermaid_png()`.

---

## Synthese des concepts abordes

| Partie | Concept | Mecanisme central |
|---|---|---|
| 1 | Graphe minimal | `StateGraph`, `add_node`, `add_edge`, `MessagesState` |
| 2 | Workflow sequentiel | Enchainement de plusieurs nodes via `add_edge` |
| 3 | Reducer | `Annotated[list[...], add]` — fusion plutot qu'ecrasement |
| 4 | Etat de type message | Accumulation automatique de l'historique de la conversation |
| 5 | Branchement conditionnel | `add_conditional_edges` associe a une fonction routeur `Literal[...]` |
| 6 | Boucle | Un node qui se rappelle lui-meme jusqu'a une condition d'arret |