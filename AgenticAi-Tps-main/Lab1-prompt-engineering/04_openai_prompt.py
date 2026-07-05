from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


load_dotenv(override=True)

model = ChatOpenAI(model="gpt-5.2", temperature=0)

response = model.invoke(
    [
        {"role": "system", "content": "You are a helpful assistant. The output should be in Markdown."},
        {"role": "user", "content": "Comment fonctionne un agent IA dans le cadre des grands modèles de langage ?"},
    ]
)

print(response.content)
