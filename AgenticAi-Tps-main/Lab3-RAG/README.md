# LAB 3 : Generation Augmentee par Recuperation (RAG)

**Master BDCC — SMA et IAD | Prof. RETAL SARA**

## But du TP

Mettre en oeuvre le pattern **RAG (Retrieval-Augmented Generation)** avec LangChain, afin de permettre a un agent base sur un LLM de repondre a des questions en s'appuyant sur des sources de donnees externes : un fichier PDF ainsi qu'une base de donnees SQL.

---

## Organisation du projet

```
Lab3-RAG/
├── part1_rag_pdf.py               # Partie 1 : Agent RAG sur PDF
├── part2_sql_agent.py             # Partie 2 : Agent SQL sur SQLite
├── acmecorp-employee-handbook.pdf # Document source (manuel employe)
└── Chinook.db                     # Base de donnees SQLite (musique)
```

---

## Prerequis

- Python >= 3.10
- [Ollama](https://ollama.com/) avec le modele `llama3.2:3b` (`ollama pull llama3.2:3b`)
- Les dependances suivantes doivent etre installees :

```bash
pip install langchain langchain-community langchain-ollama langgraph \
            sentence-transformers pypdf sqlalchemy
```

---

## Partie 1 — Agent RAG applique a un PDF

**Fichier :** `part1_rag_pdf.py`

### Chaine de traitement RAG

```
PDF → Lecture → Decoupage → Vectorisation → VectorStore → Recherche semantique → Agent
```

### Detail des etapes

| Etape | Outil utilise | Role |
|---|---|---|
| Lecture | `PyPDFLoader` | Extrait le texte page apres page |
| Decoupage | `RecursiveCharacterTextSplitter` | Divise le texte en morceaux (1000 caracteres, chevauchement de 200) |
| Vectorisation | `HuggingFaceEmbeddings` (all-MiniLM-L6-v2) | Transforme chaque morceau en vecteur |
| Stockage vectoriel | `InMemoryVectorStore` | Conserve et indexe les vecteurs en memoire |
| Recherche | `similarity_search()` | Recupere les morceaux les plus proches de la question |
| Agent | `create_react_agent` + outil `search_handbook` | Formule la reponse a partir du contexte recupere |

### Lancement

```bash
python part1_rag_pdf.py
```

### Sortie attendue

```
Pages chargées : N
Nombre de chunks : N
Documents indexés : N

--- Résultat de la recherche sémantique ---
page_content='... vacation policy ...' metadata={'page': X, ...}

--- Réponse de l'Agent RAG ---
Based on the employee handbook, employees in their first year receive X days of vacation...
```

### Fonctionnement de l'agent RAG

```
Question de l'utilisateur
     │
     ▼
  Agent LLM (llama3.2:3b)
     │
     └── outil : search_handbook(query)
                    │
                    ▼
           InMemoryVectorStore
           similarity_search()
                    │
                    ▼
           morceau le plus pertinent
           (acmecorp-employee-handbook.pdf)
                    │
                    ▼
           Réponse basée sur le contexte
```

---

## Partie 2 — Agent SQL applique a une base SQLite

**Fichier :** `part2_sql_agent.py`  
**Base de donnees :** `Chinook.db` (base musicale contenant artistes, albums, pistes, etc.)

### Chaine de traitement de l'agent SQL

```
Question en langage naturel → Agent LLM → outil sql_query → SQLite → Résultat → Réponse en langage naturel
```

### Lancement

```bash
python part2_sql_agent.py
```

### Sortie attendue

```
--- Test du tool sql_query ---
[(1, 'AC/DC'), (2, 'Accept'), (3, 'Aerosmith'), ...]

--- Réponse de l'Agent SQL ---
Here are the first 5 artists in the database:
1. AC/DC
2. Accept
3. Aerosmith
4. Alanis Morissette
5. Alice In Chains
```

### Schema de la base Chinook mobilise

```sql
Table Artist:
  - ArtistId  INTEGER (PK)
  - Name      TEXT
```

### Consignes donnees a l'agent SQL

L'agent suit des regles precises :
- Faire appel **exclusivement** a l'outil `sql_query`
- Ne jamais inventer de reponse — signaler clairement quand l'information est absente
- Formuler les resultats dans un **langage naturel clair et lisible**

---

## Mise en parallele des deux approches

| | Partie 1 — RAG sur PDF | Partie 2 — Agent SQL |
|---|---|---|
| **Source de donnees** | Fichier PDF | Base SQLite |
| **Indexation** | Embeddings vectoriels | Aucune indexation |
| **Type de recherche** | Similarite semantique | Requetes SQL precises |
| **Role du LLM** | Synthetiser le contexte recupere | Generer des requetes SQL |
| **Cas d'usage ideal** | Questions ouvertes sur des documents | Donnees structurees et precises |

---

## Le principe du RAG

```
Sans RAG :   Question → LLM (connaissances limitées) → Réponse potentiellement erronée

Avec RAG :   Question → Récupération (documents pertinents)
                              │
                              ▼
                    LLM + Contexte récupéré → Réponse précise et sourcée
```