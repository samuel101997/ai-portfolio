from langchain_ollama import ChatOllama
from agent.prompts import SYSTEM_PROMPT
from agent.tools import get_tools
from langchain_classic.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from config import MODEL_NAME, OLLAMA_BASE_URL, MAX_ITERATIONS, VERBOSE
import logging
import json
from datetime import datetime

# Set up logging
logging.basicConfig(
    filename="agent_log.json",
    level=logging.INFO,
    format="%(message)s"
)

def log_step(step_type, content):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "type": step_type,
        "content": content
    }
    logging.info(json.dumps(entry))


def create_agent():
    llm = ChatOllama(model=MODEL_NAME, base_url=OLLAMA_BASE_URL)
    tools = get_tools()

    template = """Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

""" + SYSTEM_PROMPT + """

Question: {input}
Thought: {agent_scratchpad}"""

    prompt = PromptTemplate(
        template=template,
        input_variables=["input", "agent_scratchpad"],
        partial_variables={"tools": "", "tool_names": ""}
    )

    agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)

    executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=VERBOSE,
        max_iterations=MAX_ITERATIONS,
        handle_parsing_errors="Check your output and make sure it conforms to the expected format. Always end with 'Final Answer: <your answer>'"
    )

    return executor

def run_agent(query):
    log_step("query", query)
    executor = create_agent()
    try:
        result = executor.invoke({"input": query})
        log_step("result", result["output"])
        return result["output"]
    except json.JSONDecodeError as e:
        log_step("parse_error", str(e))
        return "The agent completed research but had trouble formatting the response. Please try again with a more specific query."
    except Exception as e:
        log_step("error", str(e))
        return f"Agent encountered an error: {str(e)}"