from dotenv import load_dotenv
import os
from langchain.prompts import PromptTemplate
from langchain_core import messages
from langchain import chains
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
import subprocess

load_dotenv()
chat_model = ChatOpenAI(
    model=os.environ["OPENROUTER_MODEL"],
    openai_api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url=os.environ["OPENROUTER_BASE_URL"],
    max_tokens=1024,
    temperature=0.7,
)

input = """https://www.saucedemo.com"""
recorded_actions = """"[
  {
    "type": "click",
    "xpath": "//*[@id=\"user-name\"]"
  },
  {
    "type": "input",
    "value": "standard_user",
    "xpath": "//*[@id=\"user-name\"]"
  },
  {
    "type": "click",
    "xpath": "//*[@id=\"password\"]"
  },
  {
    "type": "input",
    "value": "s",
    "xpath": "//*[@id=\"password\"]"
  },
  {
    "type": "input",
    "value": "se",
    "xpath": "//*[@id=\"password\"]"
  },
  {
    "type": "input",
    "value": "sec",
    "xpath": "//*[@id=\"password\"]"
  },
  {
    "type": "input",
    "value": "secr",
    "xpath": "//*[@id=\"password\"]"
  },
  {
    "type": "input",
    "value": "secre",
    "xpath": "//*[@id=\"password\"]"
  },
  {
    "type": "input",
    "value": "secret",
    "xpath": "//*[@id=\"password\"]"
  },
  {
    "type": "input",
    "value": "secret_",
    "xpath": "//*[@id=\"password\"]"
  },
  {
    "type": "input",
    "value": "secret_S",
    "xpath": "//*[@id=\"password\"]"
  },
  {
    "type": "input",
    "value": "secret_Sa",
    "xpath": "//*[@id=\"password\"]"
  },
  {
    "type": "input",
    "value": "secret_Sau",
    "xpath": "//*[@id=\"password\"]"
  },
  {
    "type": "input",
    "value": "secret_Sauc",
    "xpath": "//*[@id=\"password\"]"
  },
  {
    "type": "input",
    "value": "secret_Sauce",
    "xpath": "//*[@id=\"password\"]"
  },
  {
    "type": "click",
    "xpath": "//*[@id=\"root\"]/DIV[1]/DIV[1]"
  },
  {
    "type": "click",
    "xpath": "//*[@id=\"login-button\"]"
  },
  {
    "type": "click",
    "xpath": "//*[@id=\"password\"]"
  },
  {
    "type": "input",
    "value": "secret_Sauc",
    "xpath": "//*[@id=\"password\"]"
  },
  {
    "type": "input",
    "value": "secret_Sau",
    "xpath": "//*[@id=\"password\"]"
  },
  {
    "type": "input",
    "value": "secret_Sa",
    "xpath": "//*[@id=\"password\"]"
  },
  {
    "type": "input",
    "value": "secret_S",
    "xpath": "//*[@id=\"password\"]"
  },
  {
    "type": "input",
    "value": "secret_",
    "xpath": "//*[@id=\"password\"]"
  },
  {
    "type": "input",
    "value": "secret",
    "xpath": "//*[@id=\"password\"]"
  },
  {
    "type": "input",
    "value": "secre",
    "xpath": "//*[@id=\"password\"]"
  },
  {
    "type": "input",
    "value": "secr",
    "xpath": "//*[@id=\"password\"]"
  },
  {
    "type": "input",
    "value": "sec",
    "xpath": "//*[@id=\"password\"]"
  },
  {
    "type": "input",
    "value": "se",
    "xpath": "//*[@id=\"password\"]"
  },
  {
    "type": "input",
    "value": "s",
    "xpath": "//*[@id=\"password\"]"
  },
  {
    "type": "input",
    "value": "",
    "xpath": "//*[@id=\"password\"]"
  },
  {
    "type": "input",
    "value": "e",
    "xpath": "//*[@id=\"password\"]"
  },
  {
    "type": "input",
    "value": "",
    "xpath": "//*[@id=\"password\"]"
  },
  {
    "type": "input",
    "value": "s",
    "xpath": "//*[@id=\"password\"]"
  },
  {
    "type": "input",
    "value": "se",
    "xpath": "//*[@id=\"password\"]"
  },
  {
    "type": "input",
    "value": "sec",
    "xpath": "//*[@id=\"password\"]"
  },
  {
    "type": "input",
    "value": "secr",
    "xpath": "//*[@id=\"password\"]"
  },
  {
    "type": "input",
    "value": "secre",
    "xpath": "//*[@id=\"password\"]"
  },
  {
    "type": "input",
    "value": "secret",
    "xpath": "//*[@id=\"password\"]"
  },
  {
    "type": "input",
    "value": "secret_",
    "xpath": "//*[@id=\"password\"]"
  },
  {
    "type": "input",
    "value": "secret_s",
    "xpath": "//*[@id=\"password\"]"
  },
  {
    "type": "input",
    "value": "secret_sa",
    "xpath": "//*[@id=\"password\"]"
  },
  {
    "type": "input",
    "value": "secret_sau",
    "xpath": "//*[@id=\"password\"]"
  },
  {
    "type": "input",
    "value": "secret_sauc",
    "xpath": "//*[@id=\"password\"]"
  },
  {
    "type": "input",
    "value": "secret_sauce",
    "xpath": "//*[@id=\"password\"]"
  },
  {
    "type": "click",
    "xpath": "//*[@id=\"login-button\"]"
  },
  {
    "type": "click",
    "xpath": "//*[@id=\"header_container\"]/DIV[1]/DIV[2]/DIV[1]"
  },
  {
    "type": "click",
    "xpath": "//*[@id=\"react-burger-menu-btn\"]"
  },
  {
    "type": "click",
    "xpath": "//*[@id=\"inventory_sidebar_link\"]"
  },
  {
    "type": "click",
    "xpath": "//*[@id=\"root\"]/DIV[1]/DIV[1]"
  },
  {
    "type": "click",
    "xpath": "//*[@id=\"root\"]/DIV[1]/DIV[2]/DIV[1]"
  },
  {
    "type": "click",
    "xpath": "//*[@id=\"user-name\"]"
  },
  {
    "type": "click",
    "xpath": "//*[@id=\"login_button_container\"]/DIV[1]/FORM[1]/DIV[1]/svg[1]/path[1]"
  },
  {
    "type": "click",
    "xpath": "//*[@id=\"login_button_container\"]/DIV[1]/FORM[1]/DIV[1]/svg[1]/path[1]"
  },
  {
    "type": "click",
    "xpath": "//*[@id=\"login_button_container\"]/DIV[1]/FORM[1]/DIV[2]/svg[1]/path[1]"
  },
  {
    "type": "click",
    "xpath": "//*[@id=\"user-name\"]"
  },
  {
    "type": "input",
    "value": "standard_user",
    "xpath": "//*[@id=\"user-name\"]"
  },
  {
    "type": "click",
    "xpath": "//*[@id=\"password\"]"
  },
  {
    "type": "input",
    "value": "s",
    "xpath": "//*[@id=\"password\"]"
  },
  {
    "type": "input",
    "value": "se",
    "xpath": "//*[@id=\"password\"]"
  },
  {
    "type": "input",
    "value": "sec",
    "xpath": "//*[@id=\"password\"]"
  },
  {
    "type": "input",
    "value": "secr",
    "xpath": "//*[@id=\"password\"]"
  },
  {
    "type": "input",
    "value": "secre",
    "xpath": "//*[@id=\"password\"]"
  },
  {
    "type": "input",
    "value": "secret",
    "xpath": "//*[@id=\"password\"]"
  },
  {
    "type": "input",
    "value": "secret_",
    "xpath": "//*[@id=\"password\"]"
  },
  {
    "type": "input",
    "value": "secret_s",
    "xpath": "//*[@id=\"password\"]"
  },
  {
    "type": "input",
    "value": "secret_sa",
    "xpath": "//*[@id=\"password\"]"
  },
  {
    "type": "input",
    "value": "secret_sau",
    "xpath": "//*[@id=\"password\"]"
  },
  {
    "type": "input",
    "value": "secret_sauc",
    "xpath": "//*[@id=\"password\"]"
  },
  {
    "type": "input",
    "value": "secret_sauce",
    "xpath": "//*[@id=\"password\"]"
  },
  {
    "type": "click",
    "xpath": "//*[@id=\"login-button\"]"
  },
  {
    "type": "click",
    "xpath": "//*[@id=\"item_4_title_link\"]/DIV[1]"
  },
  {
    "type": "click",
    "xpath": "//*[@id=\"add-to-cart\"]"
  },
  {
    "type": "click",
    "xpath": "//*[@id=\"shopping_cart_container\"]/A[1]"
  },
  {
    "type": "click",
    "xpath": "//*[@id=\"checkout\"]"
  },
  {
    "type": "click",
    "xpath": "//*[@id=\"first-name\"]"
  },
  {
    "type": "input",
    "value": "V",
    "xpath": "//*[@id=\"first-name\"]"
  },
  {
    "type": "input",
    "value": "Vi",
    "xpath": "//*[@id=\"first-name\"]"
  },
  {
    "type": "input",
    "value": "Vis",
    "xpath": "//*[@id=\"first-name\"]"
  },
  {
    "type": "input",
    "value": "Vish",
    "xpath": "//*[@id=\"first-name\"]"
  },
  {
    "type": "input",
    "value": "Vishn",
    "xpath": "//*[@id=\"first-name\"]"
  },
  {
    "type": "input",
    "value": "Vishnu",
    "xpath": "//*[@id=\"first-name\"]"
  },
  {
    "type": "click",
    "xpath": "//*[@id=\"last-name\"]"
  },
  {
    "type": "input",
    "value": "N",
    "xpath": "//*[@id=\"last-name\"]"
  },
  {
    "type": "input",
    "value": "Na",
    "xpath": "//*[@id=\"last-name\"]"
  },
  {
    "type": "input",
    "value": "Nan",
    "xpath": "//*[@id=\"last-name\"]"
  },
  {
    "type": "input",
    "value": "Nand",
    "xpath": "//*[@id=\"last-name\"]"
  },
  {
    "type": "input",
    "value": "Nandu",
    "xpath": "//*[@id=\"last-name\"]"
  },
  {
    "type": "input",
    "value": "Nandur",
    "xpath": "//*[@id=\"last-name\"]"
  },
  {
    "type": "input",
    "value": "Nandurk",
    "xpath": "//*[@id=\"last-name\"]"
  },
  {
    "type": "input",
    "value": "Nandurka",
    "xpath": "//*[@id=\"last-name\"]"
  },
  {
    "type": "input",
    "value": "Nandurkar",
    "xpath": "//*[@id=\"last-name\"]"
  },
  {
    "type": "click",
    "xpath": "//*[@id=\"postal-code\"]"
  },
  {
    "type": "input",
    "value": "9",
    "xpath": "//*[@id=\"postal-code\"]"
  },
  {
    "type": "input",
    "value": "92",
    "xpath": "//*[@id=\"postal-code\"]"
  },
  {
    "type": "input",
    "value": "920",
    "xpath": "//*[@id=\"postal-code\"]"
  },
  {
    "type": "input",
    "value": "9209",
    "xpath": "//*[@id=\"postal-code\"]"
  },
  {
    "type": "input",
    "value": "92092",
    "xpath": "//*[@id=\"postal-code\"]"
  },
  {
    "type": "click",
    "xpath": "//*[@id=\"checkout_info_container\"]/DIV[1]/FORM[1]"
  },
  {
    "type": "click",
    "xpath": "//*[@id=\"continue\"]"
  },
  {
    "type": "click",
    "xpath": "//*[@id=\"finish\"]"
  }
]"""
prompt = """ the website is {input}. 
You are an expert QA automation engineer. Convert the following {recorded_actions} into a Selenium test script using Python. Follow these rules:
Use chromedriver as the browser. 
Use only the last key for any input field. 
sleep for 2 seconds after finishing all the actions. 
Here are the imports: 
from selenium import webdriver, 
from selenium.webdriver.chrome.service import Service, 
from selenium.webdriver.common.by import By, 
from selenium.webdriver.common.keys import Keys, 
import time

Input JSON:
```json
{recorded_actions}
```
Output requirements:
- Only generate Python code
- Include necessary imports
- Use Chrome WebDriver
- Add comments for each action group
do not include this line "Here's the Python Selenium test script using Pytest that follows your requirements:
do not include this ```python ```
"""
prompt_template = PromptTemplate.from_template(template=prompt)
chain = prompt_template | chat_model | StrOutputParser()
output = chain.invoke(input={"input": input, "recorded_actions" : recorded_actions})
print(output)

generated_code = "generated_code.py"
with open(generated_code, "w") as f:
    f.write(output)
print(f"✅ Code saved to {generated_code}")

try:
    result = subprocess.run(
        ["python", generated_code],
        check=True,
        text=True,
        capture_output=True
    )
    print("\n🟢 Execution Output:")
    print(result.stdout)
except subprocess.CalledProcessError as e:
    print("\n🔴 Execution Failed:")
    print(f"Error Code: {e.returncode}")
    print(f"Error Message:\n{e.stderr}")

