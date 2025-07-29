from langchain_core.messages import SystemMessage, HumanMessage
from openai import OpenAI
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import json
import os
import subprocess
import sys
#try with www.amazon.in
# Load environment variables
load_dotenv()

# Initialize OpenAI client
model = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("OPENROUTER_BASE_URL")
)

# Web inspection function (unchanged from your original)
def inspect_tool(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(url)
        driver.implicitly_wait(5)
        result = {
            "buttons": [],
            "input_boxes": [],
            "hyperlinks": []
        }

        def generate_selectors(element, element_type):
            tag = element.tag_name
            id_val = element.get_attribute('id')
            css_selector = tag
            xpath = f"//{tag}"

            classes = element.get_attribute('class')
            if classes:
                class_list = classes.split()
                css_selector += '.' + '.'.join(class_list)

            attributes = []
            if element_type == 'button':
                attributes = ['name', 'type', 'value', 'aria-label']
            elif element_type == 'input_box':
                attributes = ['name', 'type', 'placeholder', 'value', 'aria-label']
            elif element_type == 'hyperlink':
                attributes = ['href', 'title', 'aria-label']

            predicates = []
            for attr in attributes:
                value = element.get_attribute(attr)
                if value:
                    css_selector += f"[{attr}='{value}']"
                    predicates.append(f"@{attr}='{value}'")

            if predicates:
                xpath += f"[{' and '.join(predicates)}]"

            return css_selector, xpath

        buttons = driver.find_elements(
            By.XPATH,
            "//button | //input[@type='button' or @type='submit' or @type='reset' or @type='image']"
        )
        for btn in buttons:
            id_val = btn.get_attribute('id') or None
            css_selector, xpath = generate_selectors(btn, 'button')
            result["buttons"].append({
                "id": id_val,
                "css_selector": css_selector,
                "xpath": xpath
            })

        input_boxes = driver.find_elements(
            By.XPATH,
            "//input[@type='text' or @type='password' or @type='email' or @type='number' " +
            "or @type='search' or @type='tel' or @type='url'] | //textarea"
        )
        for inp in input_boxes:
            id_val = inp.get_attribute('id') or None
            css_selector, xpath = generate_selectors(inp, 'input_box')
            result["input_boxes"].append({
                "id": id_val,
                "css_selector": css_selector,
                "xpath": xpath
            })

        hyperlinks = driver.find_elements(By.TAG_NAME, "a")
        for link in hyperlinks:
            id_val = link.get_attribute('id') or None
            css_selector, xpath = generate_selectors(link, 'hyperlink')
            result["hyperlinks"].append({
                "id": id_val,
                "css_selector": css_selector,
                "xpath": xpath
            })

        return result

    finally:
        driver.quit()

def run_script(generated_code: str):
    try:
        # Save the generated code to a file
        with open("generated_test.py", "w") as f:
            f.write(generated_code)

        # Execute the script
        result = subprocess.run(
            [sys.executable, "generated_test.py"],
            capture_output=True,
            text=True,
            check=True
        )

        return {
            "status": "success",
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }
    except subprocess.CalledProcessError as e:
        return {
            "status": "error",
            "stdout": e.stdout,
            "stderr": e.stderr,
            "returncode": e.returncode
        }
    except Exception as e:
        return {
            "status": "exception",
            "error": str(e)
        }

# Define function specification for OpenAI
tools = [
    {
    "type": "function",
    "function": {
        "name": "inspect_tool",
        "description": "Inspect a webpage and retrieve information about buttons, input boxes, and hyperlinks",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The URL of the webpage to inspect"
                }
            },
            "required": ["url"],
            "additionalProperties": False
        },
        "strict": True
    }
},
    {
        "type": "function",
        "function": {
            "name": "run_script_tool",
            "description": "Execute generated Selenium Python code and return the execution results",
            "parameters": {
                "type": "object",
                "properties": {
                    "generated_code": {
                        "type": "string",
                        "description": "The Python code to execute"
                    }
                },
                "required": ["code"],
                "additionalProperties": False
            },
            "strict": True
        }
    }
]

# User request about webpage inspection
"""messages = [{"role": "user", "content": "Inspect the elements on Sauce Demo: https://www.saucedemo.com"
                                        "1. Login with username (standard_user) and password (secret_sauce)\n"
                                        "2. Add any item to cart\n"
                                        "3. Checkout and order that item by filling in details. You can use random \n"
                                        "Use chromedriver as the browser. Search html elements by ID.\n"
                                        "Add explicit waits after each page navigation using WebDriverWait and expected_conditions.\n"
                                        "Handle potential errors with try/except blocks.\n"
                                        "After login, wait for inventory container to be visible before adding to cart.\n"
                                        "After adding to cart, wait for cart badge to update before proceeding.\n"
                                        "After checkout click, wait for checkout form to be visible.\n"
                                        "Sleep for 2 seconds only at the very end.\n"
                                        "Sleep for 5 seconds after finishing all the actions.\n"
                                        "Imports: from selenium import webdriver, from selenium.webdriver.chrome.service import Service, "
                                        "from selenium.webdriver.common.by import By, from selenium.webdriver.common.keys import Keys, import time\n"
                                        "from selenium.webdriver.support.ui import WebDriverWait\n"
                                        "from selenium.webdriver.support import expected_conditions as EC\n"
                                        "Only include the python code in response with no comments."
                                        "Remember to remove 'python' at top of the script - very important so that the script can be run as a subprocess."
                                        "run the script after generating the code."}]"""

system_prompt = """"You are test automation engineer. Use tools - inspect tool, run script to perform actions."
                    "Write selenium code to test actions performed on a website (given by user as input)"
                    "ALWAYS call `inspect_page(url)` to reach the correct sub-page and get filtered DOM JSON of any url before generating any code.
                    "Always call `run_script(code)` for executing any python code."
                    "Use chromedriver as the browser. Search html elements by ID.\n"
                    "Add explicit waits after each page navigation using WebDriverWait and expected_conditions.\n"
                    "Handle potential errors with try/except blocks.\n"
                    "Sleep for 2 seconds only at the very end.\n"
                    "Sleep for 5 seconds after finishing all the actions.\n"
                    "Imports: from selenium import webdriver, from selenium.webdriver.chrome.service import Service, "
                    "from selenium.webdriver.common.by import By, from selenium.webdriver.common.keys import Keys, import time\n"
                    "from selenium.webdriver.support.ui import WebDriverWait\n"
                    "from selenium.webdriver.support import expected_conditions as EC\n"
                    "Only include the python code in response with no comments."
                    "Remember to remove 'python' at top of the script - very important so that the script can be run as a subprocess."
                    "run the script after generating the code."""

"""user_prompt = Inspect the elements on Sauce Demo: https://www.saucedemo.com
                                        "1. Login with username (standard_user) and password (secret_sauce)\n"
                                        "2. Add any item to cart\n"
                                        "3. Checkout and order that item by filling in details. You can use random \n"""
user_prompt = """Inspect the elements on amazon: https://www.amazon.in. Then register on the website with a new account. 
                 Fill in a valid username and password to create this new account."""

messages = [
    SystemMessage(content=system_prompt),
    HumanMessage(content=user_prompt)
]

# First API call - detect function need
completion = model.chat.completions.create(
    model="deepseek/deepseek-chat-v3-0324:free",
    messages=messages,
    tools=tools,
    tool_choice="auto",
)
print(completion)

# Process tool calls in a loop
while True:
    message = completion.choices[0].message
    print(message)
    tool_calls = message.tool_calls if message.tool_calls else []

    if not tool_calls:
        # No more tool calls needed
        print("\nFinal Response:")
        print(message.content)
        break

    # Process each tool call
    for tool_call in tool_calls:
        function_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        print(function_name, arguments)

        if function_name == "inspect_tool":
            print(f"\nInspecting: {arguments['url']}")
            result = inspect_tool(arguments['url'])
            result_content = json.dumps(result, indent=2)
        elif function_name == "run_script_tool":
            print("\nExecuting Selenium script...")
            result = run_script(arguments['generated_code'])
            result_content = json.dumps(result, indent=2)
        else:
            result_content = "Unknown function called"

        # Append tool response to messages
        messages.append({
            "role": "assistant",
            "content": None,
            "tool_calls": [tool_call]
        })
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "name": function_name,
            "content": result_content
        })

    # Get next completion
    completion = model.chat.completions.create(
        model="deepseek/deepseek-chat-v3-0324:free",
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )