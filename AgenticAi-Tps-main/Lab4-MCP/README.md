# LAB 4 : Le Model Context Protocol (MCP)

**Master BDCC — SMA et IAD | Prof. RETAL SARA**

## But du TP

Mettre en place le **Model Context Protocol (MCP)** en le combinant avec LangChain, afin de connecter des agents bases sur un LLM a des serveurs MCP, qu'ils soient locaux ou distants, via plusieurs types de transport (stdio, HTTP en streaming).

---

## Organisation du projet

```
Lab4-MCP/
├── mcp_local_server.py      # Serveur MCP local (stdio) — tools + resources + prompts
├── mcp_http_server.py       # Serveur MCP HTTP local (streamable-http)
├── agentMCP.py              # Partie 1 : Agent avec serveur MCP local
├── agentMCPTime.py          # Partie 2 : Agent avec serveur MCP de temps
├── agentMCPDistant.py       # Partie 3 : Agent avec serveur MCP distant (HTTP)
├── pyproject.toml
├── .env.example
└── .gitignore
```

---

## Prerequis

- Python >= 3.10
- [uv](https://docs.astral.sh/uv/) installe sur la machine
- [Ollama](https://ollama.com/) avec le modele `llama3.2:3b` (`ollama pull llama3.2:3b`)
- Une cle API Tavily (`TAVILY_API_KEY`) renseignee dans le fichier `.env`

### Mise en place

```bash
# Dupliquer le fichier d'environnement
cp .env.example .env
# Completer les cles API dans .env

# Installer les dependances du projet
uv sync

# Sous Windows : installer pywin32 manuellement (pour contourner un blocage antivirus)
python -m ensurepip
pip3 install pywin32
```

---

## Contenu du TP

### Partie 1 — Serveur MCP local (stdio)

Le serveur `mcp_local_server.py` met a disposition :
- **Un outil (tool)** : `search_web` — permet une recherche web via Tavily
- **Une ressource** : le README du depot `langchain-mcp-adapters` (GitHub)
- **Un prompt** : le prompt systeme de l'assistant LangChain

```bash
uv run --active python agentMCP.py
```

**Resultat obtenu :** l'agent recupere dynamiquement les outils, ressources et prompts exposes par le serveur MCP, lance une recherche sur le web, puis formule sa reponse.

```
{'messages': [..., AIMessage(content='The langchain-mcp-adapters library is a
lightweight wrapper that makes Anthropic Model Context Protocol (MCP) tools
compatible with LangChain and LangGraph...')]}
```

---

### Partie 2 — Serveur MCP dedie au temps (time server)

Ce module s'appuie sur le package `mcp-server-time` pour fournir l'heure reelle selon le fuseau horaire demande.

```bash
uv run --active python agentMCPTime.py
```

**Resultat obtenu :**
```
The current time in Japan is 3:30 AM on Saturday (June 6th, 2026),
considering the 13-hour time difference from New York.
```

> **Remarque pour Windows :** sur cet OS, le serveur `mcp-server-time` doit etre installe directement dans le `.venv` via `pip3 install mcp-server-time` (plutot que par `uvx`), a cause d'un souci de cache lie a `pywin32`.

---

### Partie 3 — Serveur MCP distant (HTTP en streaming)

Cette partie illustre une connexion a un serveur MCP via le transport `streamable-http`. Un serveur de voyage est lance automatiquement en local, dans un thread separe.

```bash
uv run --active python agentMCPDistant.py
```

**Resultat obtenu :**
```
Serveur MCP HTTP démarré sur http://127.0.0.1:8000/mcp
Tools disponibles : ['search_flights', 'get_flight_price']

Here are the direct flight options from Rabat to Agadir on August 31st:
* Atlas Blue (AT) - Flight 601: Departing at 08:00, arriving at 09:15
* Atlas Blue (AT) - Flight 603: Departing at 14:30, arriving at 15:45
* Atlas Blue (AT) - Flight 605: Departing at 19:00, arriving at 20:15
```

---

## Fonctionnement global du MCP dans ce projet

```
Agent LLM (LangChain)
    │
    └── MultiServerMCPClient
            │
            ├── transport stdio ──────► mcp_local_server.py (sous-processus python)
            ├── transport stdio ──────► mcp-server-time (executable)
            └── streamable-http ──────► http://127.0.0.1:8000/mcp (uvicorn)
```

---

## Principales dependances utilisees

| Package | Utilite |
|---|---|
| `langchain-mcp-adapters` | Fait le lien entre le client MCP et LangChain/LangGraph |
| `mcp` | Implemente le protocole MCP |
| `fastmcp` | Simplifie la creation d'un serveur MCP |
| `mcp-server-time` | Serveur MCP fournissant l'heure par fuseau horaire |
| `langchain-ollama` | Permet d'utiliser un modele LLM local via Ollama |
| `tavily-python` | Bibliotheque de recherche web |
| `langgraph` | Sert de runtime pour l'execution de l'agent |