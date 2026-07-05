
Claude finished the response

Created a file, read a file
Created a file, read a file
Voici la reformulation du README pour le LAB 7 (agent Human-In-The-Loop).


Readme lab7 reformule
Document · MD 

# LAB 8 : Workflows avec LangGraph **Master BDCC — SMA et IAD | Prof. RETAL SARA** ## Objectif Découvrir les briques de base d'un **workflow LangGraph** : graphe d'états, nodes, edges, reducers, état de type message, branchements conditionnels et boucles. --- ## Structure du projet

pasted

reformule


Restructured documentation for consistency
Restructured documentation for consistency
Voici la reformulation du README pour le LAB 8 (Workflows avec LangGraph).


Readme lab8 reformule
Document · MD 

# LAB 9 : Agent avec LangGraph **Master BDCC — SMA et IAD | Prof. RETAL SARA** ## Objectif Construire progressivement un **agent LangGraph** complet : un LLM doté d'outils (tools), exécuté comme nœud de graphe, capable de s'arrêter pour validation humaine (HITL), de reprendre après interrup

pasted

refrormule


Created a file, read a file
Created a file, read a file
Voici la reformulation du README pour le LAB 9 (Agent avec LangGraph).


Readme lab9 reformule
Document · MD 

# TP : Agent Chef Cuisinier Personnel **Master BDCC — SMA et IAD | Prof. RETAL SARA** ## Objectif Concevoir un agent intelligent jouant le rôle d'un chef cuisinier personnel, capable de : - Recevoir la liste des ingrédients disponibles - Mémoriser les préférences et restrictions alimentai

pasted

reformule


Created a file, read a file
Created a file, read a file
Voici la reformulation du README pour le TP Agent Chef Cuisinier Personnel.


Readme chefpersonnel reformule
Document · MD 

# AI Agentic — Master BDCC Dépôt personnel regroupant l'ensemble des travaux pratiques réalisés dans le cadre du module **SMA et IAD — Master BDCC | Prof. RETAL SARA**. **Étudiante : Hajar Berchil — Master IBDCC** ## Structure | Dossier | Sujet | |---|---| | [Lab1-prompt-engineering](.

pasted

reformule ça avec suppression des linges de evaluation final :


Orchestrated suppression des lignes d'évaluation finale
Orchestrated suppression des lignes d'évaluation finale
Voici la reformulation du README principal, avec la section "Evaluation-finale" retirée (aussi bien la ligne du tableau que le détail de sa structure).


Readme principal reformule
Document · MD 





Claude is AI and can make mistakes. Please double-check responses.


Readme principal reformule · MD
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
 
