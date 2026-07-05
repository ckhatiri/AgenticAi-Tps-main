# TP Agents avec LangChain
 
Ce depot contient l'implementation du TP `Chef Personnel`, base sur le sujet remis par le professeur.
 
## But du TP
 
Developper un agent capable de :
- recuperer la liste des ingredients disponibles
- retenir les preferences de l'utilisateur
- faire appel a un outil de recherche web lorsque cela est necessaire
- suggerer une ou plusieurs recettes adaptees
## Organisation des fichiers
 
- `chef_personnel_agent.py` : le script principal de l'agent
- `requirements.txt` : liste des dependances Python
- `.env.example` : modele de fichier de configuration
- `2 TP Agents avec Langchain.docx` et `.odt` : enonce original du TP
## Installation des dependances
 
```bash
pip install -r requirements.txt
```
 
## Configuration
 
Dupliquer `.env.example` en `.env`, puis renseigner les champs suivants :
 
```env
OLLAMA_MODEL=llama3.2:3b
TAVILY_API_KEY=...
APP_MODE=interactive
OLLAMA_TEMPERATURE=0
```
 
## Lancer le programme
 
En mode interactif :
 
```bash
python chef_personnel_agent.py
```
 
En mode demonstration :
 
```bash
APP_MODE=demo python chef_personnel_agent.py
```
 
## A savoir
 
- La cle `TAVILY_API_KEY` n'est pas obligatoire, mais elle est requise pour effectuer une veritable recherche sur le web.
- La valeur `OLLAMA_MODEL` doit correspondre a un modele deja installe localement sur Ollama.
- Les performances dependent avant tout du modele local selectionne.
## Captures d'ecran
![Exercise 1](images/WindowsTerminal_1.png)
![Exercise 2](images/WindowsTerminal_2.png)
![Exercise 3](images/WindowsTerminal_3.png)
![Exercise 4](images/WindowsTerminal_4.png)