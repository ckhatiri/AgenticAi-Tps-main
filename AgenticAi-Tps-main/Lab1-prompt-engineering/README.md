# TP Ingenierie des Prompts
 
Ce projet a ete structure a partir du sujet fourni dans le document `1 TP Ingenierie des prompts.docx`.
 
## Contenu du projet
 
- `01_tokenisation.py` : illustre la tokenisation a l'aide de la bibliotheque `tiktoken`
- `02_ollama_prompt.py` : envoie un prompt basique via Ollama
- `03_groq_prompt.py` : envoie un prompt basique via Groq
- `04_openai_prompt.py` : envoie un prompt basique via OpenAI
- `05_aspect_sentiment_json.py` : realise une analyse de sentiment et retourne le resultat au format JSON
- `06_image_generation.py` : genere une image
- `07_image_description.py` : produit une description de l'image `rag.png`
## Mise en place avec uv
 
Creer et synchroniser l'environnement virtuel :
 
```bash
uv venv
uv sync
```
 
Pour activer l'environnement :
 
Sur Windows (PowerShell) :
 
```powershell
.venv\Scripts\Activate.ps1
```
 
Sur bash (Linux/macOS) :
 
```bash
source .venv/bin/activate
```
 
## Configuration des cles API
 
Dupliquer le fichier `.env.example` en `.env`, puis completer les valeurs suivantes :
 
```env
OPENAI_API_KEY=...
GROQ_API_KEY=...
OLLAMA_MODEL=llama3.2:3b
```
 
## Lancement des scripts
 
Chaque script peut etre execute independamment :
 
```bash
python 01_tokenisation.py
python 02_ollama_prompt.py
python 03_groq_prompt.py
python 04_openai_prompt.py
python 05_aspect_sentiment_json.py
python 06_image_generation.py
python 07_image_description.py
```
 
## A savoir
 
- Le script `01_tokenisation.py` fonctionne sans aucune cle API.
- Le script `02_ollama_prompt.py` necessite qu'un serveur Ollama soit lance et qu'un modele local soit deja installe.
- Les scripts `03` a `07` requierent des cles API valides pour fonctionner.