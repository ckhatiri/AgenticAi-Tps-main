import json

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


load_dotenv(override=True)

system_message = """
Réalisez une analyse de sentiment orientée aspects sur les commentaires d'utilisateurs
concernant des ordinateurs portables fournis en entrée.

Les aspects à identifier sont : screen (écran), keyboard (clavier) et pad (pavé tactile).

Pour chaque commentaire :
- Détectez lesquels de ces trois aspects sont mentionnés.
- Assignez une polarité (positive, negative ou neutral) à chaque aspect identifié.
- Retournez votre analyse sous forme d'objet JSON avec les champs :
  - category : liste des aspects détectés
  - polarity : liste des polarités correspondantes
- Si un aspect n'est pas évoqué dans le commentaire, attribuez-lui la polarité neutral.
"""

llm = ChatOpenAI(
    model="gpt-5.2",
    temperature=0,
    model_kwargs={"response_format": {"type": "json_object"}},
)

resp = llm.invoke(
    [
        {"role": "system", "content": system_message},
        {
            "role": "user",
            "content": "L'affichage est excellent, mais le pavé tactile me déçoit vraiment. Le clavier reste correct.",
        },
    ]
)

print(resp.content)

result = json.loads(resp.content)
print("\nJSON parse:", result)
print("Premiere polarite:", result["polarity"][0])
