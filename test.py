# from dotenv import load_dotenv
# import os
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
# from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
if __name__ == "__main__":
    # load_dotenv()
    print("Hello World")
    # print(os.environ['COOL_API_KEY'])
    information = """    Narendra Damodardas Modi[a] (born 17 September 1950) is an Indian politician who has served as the prime minister of India since 2014. Modi was the chief minister of Gujarat from 2001 to 2014 and is the member of parliament (MP) for Varanasi. He is a member of the Bharatiya Janata Party (BJP) and of the Rashtriya Swayamsevak Sangh (RSS), a right-wing Hindu nationalist paramilitary volunteer organisation. He is the longest-serving prime minister outside the Indian National Congress.    """
    summary_template = """    Given the information, {information}, about a person, I want you to create:    1. Short Summary    2. Two interesting facts about them    """
    summary_prompt_template = PromptTemplate.from_template(template=summary_template)
    llm = ChatOllama(model='llama3.2')
    chain = summary_prompt_template | llm | StrOutputParser()
    res = chain.invoke(input={"information": information})
    print(res)