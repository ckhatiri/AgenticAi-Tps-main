# LAB 9 : Agent avec LangGraph

**Master BDCC — SMA et IAD | Prof. RETAL SARA**

## But du TP

Batir, etape par etape, un **agent LangGraph** complet : un LLM equipe d'outils (tools), fonctionnant comme un noeud de graphe, capable de se mettre en pause pour une validation humaine (HITL), de reprendre son execution apres une interruption, de conserver un historique de checkpoints, et de "forker" — c'est-a-dire revenir a un etat passe pour relancer l'execution a partir d'un etat modifie.

---

## Organisation du projet

```
Lab9-Agent_avec_LangGraph/
├── tools_setup.py        # Partie 1 : LLM local (Ollama) + tools arithmétiques
├── agent_node.py         # Partie 2 : agent comme nœud de graphe (llm_call / tool_node)
├── hitl_workflow.py      # Partie 3 : workflow @entrypoint/@task avec interrupt() (HITL)
├── tp_advanced_agent.py  # Partie 4 : TP — agent complet (tools + HITL + historique + fork)
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

## Partie 1 — LLM local muni d'outils (`tools_setup.py`)

Trois outils arithmetiques (`add`, `multiply`, `divide`) sont rattaches au modele Ollama grace a `bind_tools` :

```python
@tool
def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b

tools = [add, multiply, divide]
tools_by_name = {t.name: t for t in tools}
model_with_tools = model.bind_tools(tools)
```

Ce module sert de base aux parties suivantes — il n'est pas concu pour etre lance seul.

---

## Partie 2 — L'agent en tant que noeud LangGraph (`agent_node.py`)

L'etat (`AgentState`) contient :
- `messages` : l'historique integral, fusionne automatiquement grace au reducer `add`
- `llm_calls` : un compteur d'appels au LLM, incremente a chaque passage par `llm_call`

```
START ──► llm_call ──► should_continue ──┬──► tool_node ──► llm_call (boucle)
                                          └──► END
```

- `llm_call` : le LLM choisit soit d'appeler un outil, soit de repondre directement
- `tool_node` : execute les `tool_calls` demandes et renvoie des `ToolMessage`
- `should_continue` : redirige vers `tool_node` tant que le dernier message contient des `tool_calls`, sinon vers `END`

```bash
uv run --active python agent_node.py
```

### Resultats observes

```
--- Historique conversationnel (Add 3 and 4) ---
================================ Human Message =================================
Add 3 and 4.
================================== Ai Message ==================================
Tool Calls:
  add (...)
    a: 3
    b: 4
================================= Tool Message =================================
7
================================== Ai Message ==================================
The result of adding 3 and 4 is 7.

--- Stream 'updates' (Multiply 30 and 43) ---
{'llm_call': {'messages': [AIMessage(..., tool_calls=[{'name': 'multiply', 'args': {'a': '30', 'b': '43'}, ...}])], 'llm_calls': 1}}
{'tool_node': {'messages': [ToolMessage(content='1290', ...)]}}
{'llm_call': {'messages': [AIMessage(content='The result of multiplying 30 by 43 is 1290.', ...)], 'llm_calls': 2}}

--- Stream 'messages' (Divide 30 and 43) ---
0.6976744186046512The result of dividing 30 by 43 is approximately 0.6976.
```

**Ce qu'on en retient :** le mode `stream_mode="updates"` affiche chaque changement du graphe noeud par noeud (le LLM decide d'appeler `multiply`, l'outil repond `1290`, puis le LLM redige sa reponse finale). Le mode `stream_mode="messages"` diffuse quant a lui les tokens du LLM en direct — on y voit d'abord le resultat brut de l'outil (`0.69767...`), puis la phrase de synthese produite par le modele.

---

## Partie 3 — Workflow HITL avec `@entrypoint` / `@task` (`hitl_workflow.py`)

- `@task` transforme une fonction Python en unite d'execution isolee et asynchrone (on obtient le resultat via `.result()`)
- `@entrypoint` definit le point d'entree du workflow : il pilote les tasks, peut appeler `interrupt()` pour suspendre l'execution, et reprend ensuite via `Command(resume=...)`

```python
@task
def write_essay(topic: str) -> str:
    time.sleep(1)
    return f"Essay draft about {topic}"

@entrypoint(checkpointer=InMemorySaver())
def workflow(topic: str) -> dict:
    draft = write_essay(topic).result()
    approved = interrupt({"draft": draft, "action": "approve or reject"})
    return {"draft": draft, "approved": approved}
```

```bash
uv run --active python hitl_workflow.py
```

### Resultats observes

```
--- Première exécution (génère le brouillon, puis interrupt) ---
{'write_essay': 'Essay draft about cats'}
{'__interrupt__': (Interrupt(value={'draft': 'Essay draft about cats', 'action': 'approve or reject'}, ...),)}

--- Deuxième exécution (reprise après validation humaine) ---
{'workflow': {'draft': 'Essay draft about cats', 'approved': True}}
```

**Ce qu'on en retient :** la premiere execution genere le brouillon, puis **met en pause** le graphe via `interrupt()` — aucune reponse finale n'est encore disponible a ce stade. La seconde execution, avec le **meme** `thread_id` et `Command(resume=True)`, reprend precisement a l'endroit ou le graphe s'etait arrete et renvoie le resultat final, avec `approved: True`.

---

## Partie 4 — TP : un agent avance (`tp_advanced_agent.py`)

Cette partie rassemble tous les concepts precedents au sein d'un seul agent :

```
START ──► llm_call ──► should_continue ──┬──► approve ──► interrupt() ──┬──► tool_node ──► llm_call
                                          └──► END                       └──► END (si rejeté)
```

- `approve_node` appelle `interrupt()` pour demander une validation humaine **avant** l'execution de l'outil, puis redirige via `Command(goto="tool_node" if decision else END)`
- `agent.get_state(config)` et `get_state_history(config)` permettent de consulter les checkpoints sauvegardes
- La combinaison `agent.update_state(...)` puis `agent.invoke(None, new_config)` permet de **forker** : reprendre depuis un checkpoint anterieur avec un etat modifie

```bash
uv run --active python tp_advanced_agent.py
```

### Resultats observes

```
--- Scénario 1 : interruption avant exécution du tool ---
Interrupt payload: {'question': 'Approve tool execution?',
                    'tool_calls': [{'name': 'add', 'args': {'a': '3', 'b': '4'}, ...}]}
Done. Last message: content='The result of adding 3 and 4 is 7.'
Latest checkpoint next: ()
Number of checkpoints: 6
Most recent checkpoint id: 1f162dd2-2aab-6415-8004-57e8a11e62c2

--- Scénario 2 : rejet de l'exécution du tool ---
Interrupt payload: {'question': 'Approve tool execution?',
                    'tool_calls': [{'name': 'multiply', 'args': {'a': '30', 'b': '41'}, ...}]}
Done. Last message: content='' tool_calls=[{'name': 'multiply', 'args': {'a': '30', 'b': '41'}, ...}]
Forked: content='Multiply 30 and 41.'
```

**Ce qu'on en retient :**
- **Scenario 1 (validation acceptee)** : le graphe s'arrete avant `tool_node` pour demander une validation (`Approve tool execution?`), puis `Command(resume=True)` laisse l'execution se poursuivre normalement jusqu'a la reponse finale (`7`). Six checkpoints sont conserves pour ce thread.
- **Scenario 2 (rejet puis fork)** : `Command(resume=False)` fait passer `approve_node` directement vers `END` — l'outil **n'est jamais execute**, et le dernier message reste l'`AIMessage` contenant le `tool_call` non execute. En reprenant un checkpoint anterieur (`history[1]`, juste apres `START`) et en y injectant un nouvel etat via `update_state`, l'appel `agent.invoke(None, new_config)` **relance le graphe a partir de ce point historique** — ce qui illustre la capacite de LangGraph a revenir dans le temps et a explorer des branches d'execution alternatives.

---

## Synthese des concepts abordes

| Partie | Concept | Mecanisme central |
|---|---|---|
| 1 | LLM associe a des outils | `@tool`, `model.bind_tools(tools)` |
| 2 | Agent en tant que noeud | `llm_call` / `tool_node` / `should_continue`, reducer `add` sur `messages` |
| 3 | HITL fonctionnel | `@entrypoint`, `@task`, `interrupt()`, `Command(resume=...)` |
| 4 | Agent avance et complet | `approve_node` + `Command(goto=...)`, `get_state_history`, `update_state` (fork) |