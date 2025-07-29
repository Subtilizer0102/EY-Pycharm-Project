from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama

if __name__ == "__main__":
    llm = ChatOllama(model='llama3.2')
    input = "https://www.saucedemo.com"
    prompt = "write selenium code to perform following actions on {input}. 1. login with appropriate username (standard_user) and password (secret_sauce) 2. add any item to cart 3. checkout and order that item. Use chromedriver as the browser. search html elements by ID. and sleep for 10 seconds after finishing all the actions. Here are the imports: from selenium import webdriver, from selenium.webdriver.chrome.service import Service, from selenium.webdriver.common.by import By, from selenium.webdriver.common.keys import Keys, import time"
    prompt_template = PromptTemplate.from_template(template = prompt)
    chain = prompt_template | llm | StrOutputParser()
    result = chain.invoke(input = {"input" : input})
    print(result)
