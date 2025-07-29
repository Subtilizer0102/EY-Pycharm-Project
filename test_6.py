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

input = "https://www.saucedemo.com"
prompt = """write selenium code to perform following actions on {input} url.
 1. login with appropriate username (standard_user) and password (secret_sauce) 
 2. add any item to cart 
 3. checkout and order that item.
Use chromedriver as the browser. search html elements by ID.
sleep for 2 seconds after finishing all the actions. 
Here are the imports: 
from selenium import webdriver, 
from selenium.webdriver.chrome.service import Service, 
from selenium.webdriver.common.by import By, 
from selenium.webdriver.common.keys import Keys, 
import time
only include the python code in response and also no comments. 
remove ''' python at the start of the file."""
prompt_template = PromptTemplate.from_template(template=prompt)
chain = prompt_template | chat_model | StrOutputParser()
output = chain.invoke(input={"input": input})
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





