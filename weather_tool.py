from openai import OpenAI
import json
import requests
from dotenv import load_dotenv
import os

load_dotenv()
model = OpenAI(api_key = os.getenv("DEEPSEEK_API_KEY"), base_url=os.getenv("OPENROUTER_BASE_URL"))

def get_weather(latitude, longitude):
    response = requests.get(
    f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m")
    data = response.json()
    return data['current']['temperature_2m']

tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get current temperature for provided coordinates in celsius.",
        "parameters": {
            "type": "object",
            "properties": {
                "latitude": {"type": "number"},
                "longitude": {"type": "number"}
            },
            "required": ["latitude", "longitude"],
            "additionalProperties": False
        },
        "strict": True
    }
}]

messages = [{"role": "user", "content": "What's the weather like in Paris today?, assume coordinates."}]

completion = model.chat.completions.create(
    model="deepseek/deepseek-chat-v3-0324:free",
    messages=messages,
    tools=tools,
)
print(completion)
tool_call = completion.choices[0].message.tool_calls[0]
print(tool_call)

args = json.loads(tool_call.function.arguments)
result = get_weather(args["latitude"], args["longitude"])

messages.append(completion.choices[0].message)  # append model's function call message
messages.append({                               # append result message
    "role": "tool",
    "tool_call_id": tool_call.id,
    "content": str(result)
})

completion_2 = model.chat.completions.create(
    model="deepseek/deepseek-chat-v3-0324:free",
    messages=messages,
    tools=tools,
)

print("Completion 2: ", completion_2.choices[0].message.content)



