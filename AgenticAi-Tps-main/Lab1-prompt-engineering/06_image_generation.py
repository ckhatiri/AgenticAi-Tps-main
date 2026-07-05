import base64

from dotenv import load_dotenv
from langchain.messages import HumanMessage
from langchain_openai import ChatOpenAI


load_dotenv(override=True)

llm = ChatOpenAI(model="gpt-5.2")
llm_with_tools = llm.bind_tools([{"type": "image_generation", "quality": "high"}])

response = llm_with_tools.invoke(
    [HumanMessage(content="Génère une image d'un robot qui enseigne l'informatique dans une salle de classe futuriste.")]
)

image_block = response.content_blocks[0]
image_bytes = base64.b64decode(image_block["base64"])

with open("generated_robot_teacher.png", "wb") as output_file:
    output_file.write(image_bytes)

print("Image générée : generated_robot_teacher.png")
