from google import genai
from google.genai import types

GEMINI_API_KEY="AIzaSyA3znEN2iafUtuq59QS55fsdE-SoMjSPR4"
client = genai.Client(api_key=GEMINI_API_KEY)

conversation_history = [
    {
        "role": "user",
        "content": f"What are the three largest cities in Spain?"
    }
]

interaction1 = client.interactions.create(
    model="gemini-2.5-flash-lite",
    system_instruction="너는 빻봇이라는 이름으로 불려. 가능한 정확한 지식을 전달하도록 해. 친절하게 반말로 대답해.",
    input=conversation_history
)

print(f"Model: {interaction1.outputs[-1].text}")
conversation_history.append({"role": "model", "content": interaction1.outputs})
# response = client.models.generate_content(
#     model="gemini-2.5-flash-lite",
#     config=types.GenerateContentConfig(
#         system_instruction="너는 빻봇이라는 이름으로 불려. 가능한 정확한 지식을 전달하도록 해. 친절하게 반말로 대답해."),
#     contents="Hello there"
# )
# print(response.text)