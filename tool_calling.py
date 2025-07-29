import requests
import json

OPENWEATHER_API_KEY = "217cf3b7722af50927f170cb19bdf100"

def get_weather(city):
    """
    Fetch weather info for a given city using OpenWeatherMap API.
    Returns a summary string or error message.
    """
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }
    try:
        weather_response = requests.get(url, params=params)
        weather_response.raise_for_status()
        weather_data = weather_response.json()

        temp = weather_data["main"]["temp"]
        description = weather_data["weather"][0]["description"]
        humidity = weather_data["main"]["humidity"]
        wind_speed = weather_data["wind"]["speed"]
        return (f"The weather in {city} is {description} with a temperature of {temp}°C, "
            f"humidity at {humidity}%, and wind speed of {wind_speed} m/s.")
    except requests.RequestException as e:
        print(e)


# OpenRouter API key
API_KEY = "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"

# The URL for OpenRouter's chat completions endpoint
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Tool definition (function schema)
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather in a given city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "Name of the city to get weather for"
                    }
                },
                "required": ["city"]
            }
        }
    }
]

# Sample system and user messages
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What's the weather like in Mumbai?"}
]

#tool calling model.
model = "deepseek/deepseek-chat-v3-0324:free"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "//my-local-script",  # replace with your site or GitHub URL
    "X-Title": "Tool-Calling-Demo"
}

# Step 1: Ask the model
data = {
    "model": model,
    "messages": messages,
    "tools": tools,
    "tool_choice": "auto"  # Let the model decide
}
#first api call.
response = requests.post(API_URL, headers=headers, json = data)
response_json = response.json()
print("Model response (tool call):\n", response.json())

tool_call = response_json["choices"][0]["message"]["tool_calls"][0]
tool_args = json.loads(tool_call["function"]["arguments"])
city = tool_args["city"]

weather_result = get_weather(city)
print("Tool output:\n", weather_result)

follow_up_messages = messages + [
    {
        "role": "assistant",
        "tool_calls": [tool_call]
    },
    {
        "role": "tool",
        "tool_call_id": tool_call["id"],
        "name": tool_call["function"]["name"],
        "content": weather_result
    }
]

data2 = {
    "model": model,
    "messages": follow_up_messages,
}

response2 = requests.post(API_URL, headers=headers, json=data2)
print(json.dumps(response2.json(), indent=2))
print("Final LLM Answer:\n", response2.json()["choices"][0]["message"]["content"])

