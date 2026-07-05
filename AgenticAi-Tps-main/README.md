# AI Agentic — Master BDCC
 
Depot personnel reunissant l'ensemble des travaux pratiques realises dans le cadre du module **SMA et IAD — Master BDCC | Prof. RETAL SARA**.
 
**Etudiante : Hajar Berchil — Master IBDCC**
 
## Organisation
 
| Dossier | Thematique |
|---|---|
| [Lab1-prompt-engineering](./Lab1-prompt-engineering) | Ingenierie des prompts (tokenisation, Ollama, Groq, OpenAI, JSON, images) |
| [Lab2-langchain-agents](./Lab2-langchain-agents) | Agents avec LangChain (agent chef personnel, memoire, recherche web) |
| [Lab3-RAG](./Lab3-RAG) | RAG applique a un PDF (embeddings HuggingFace) et agent SQL (base Chinook) |
| [Lab4-MCP](./Lab4-MCP) | Model Context Protocol : stdio, serveur de temps, HTTP en streaming |
| [Lab5-LangGraph_Studio](./Lab5-LangGraph_Studio) | LangGraph Studio (visualisation et debogage d'agents) ainsi qu'un systeme Multi-Agents hierarchique |
| [Lab6-Contexte_et_Etat](./Lab6-Contexte_et_Etat) | Contexte fourni a l'invocation (`ReaderProfile`) et etat persiste (`LibraryState`) |
| [Lab7-Human_In_The_Loop](./Lab7-Human_In_The_Loop) | Agent HITL : `interrupt()`, decisions approve / reject / edit |
| [Lab8-Workflow_avec_LangGraph](./Lab8-Workflow_avec_LangGraph) | Workflows LangGraph : graphe simple, reducers, etat de type message, branchements conditionnels, boucles |
| [Lab9-Agent_avec_LangGraph](./Lab9-Agent_avec_LangGraph) | Agent LangGraph : outils, agent en tant que noeud, HITL fonctionnel (`@entrypoint`/`@task`), historique et fork |
| [TP-Chef_personnel](./TP-Chef_personnel) | Agent chef cuisinier : RAG, memoire, recherche web et prompt systeme |
 
## Prerequis communs
 
- Python >= 3.10
- [uv](https://docs.astral.sh/uv/) — gestionnaire de paquets
- [Ollama](https://ollama.com/) avec le modele `llama3.2:3b`
```bash
ollama pull llama3.2:3b
```
 
## Lancement
 
Chaque lab fonctionne de maniere autonome, avec son propre environnement virtuel :
 
```bash
cd Lab6-Contexte_et_Etat
uv sync
uv run --active python agent_context.py
uv run --active python agent_state.py
```
 
## A noter
 
- Les fichiers `.env` ne doivent jamais etre pousses sur GitHub (se referer au `.env.example` present dans chaque lab).
- Certains labs necessitent des cles API facultatives (`TAVILY_API_KEY`, `LANGSMITH_API_KEY`).
 
