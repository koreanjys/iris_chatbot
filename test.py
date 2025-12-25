from google import genai
from google.genai import types

GEMINI_API_KEY=""
client = genai.Client(api_key=GEMINI_API_KEY)

grounding_tool = types.Tool(
    google_search=types.GoogleSearch()
)
config = types.GenerateContentConfig(
    tools=[grounding_tool],
    system_instruction="Please summarize the content of the webpage provided as a URL in korean"
)
response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents="https://youtu.be/uEN7VUPxY9A?si=0hPpeOYFURYLjYGd",
    config=config,
)
print(response.text)
