from dotenv import load_dotenv
import os

from langchain import hub
from langchain.prompts import PromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from langchain_openai import ChatOpenAI
from langchain.agents import tool_calling_agent, AgentExecutor, create_tool_calling_agent
from langchain_core.tools import Tool

load_dotenv()
chat_model = ChatOpenAI(
    model=os.environ["OPENROUTER_MODEL"],
    openai_api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url=os.environ["OPENROUTER_BASE_URL"],
    max_tokens=1024,
    temperature=0.7,
)

def say_hello(name:str)->str:
    return f"Hello, {name}!"

tools = [Tool(name = "say_hello",
              func = say_hello,
              description = "USE THIS TOOL WHEN THE USER MENTIONS THEIR NAME. Input must be the user's name as a string.")]
prompt_template = ChatPromptTemplate.from_messages(messages =
                                      [SystemMessage(content = "You MUST use the 'say_hello' tool when the user provides their name. Extract ONLY the name from the input"),
                                       HumanMessagePromptTemplate.from_template("{input}"),
                                       MessagesPlaceholder(variable_name = "agent_scratchpad")])
ai_agent = create_tool_calling_agent(llm = chat_model, tools = tools, prompt = prompt_template)
executor = AgentExecutor.from_agent_and_tools(agent = ai_agent, tools = tools, verbose = True, handle_parsing_errors = True)
response = executor.invoke({"input" : "My name is Vishnu."})
print(response)



