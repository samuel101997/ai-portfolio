from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools import WikipediaQueryRun
from langchain_core.tools import Tool
from langchain_ollama import ChatOllama
from config import MODEL_NAME, OLLAMA_BASE_URL


def get_tools():
    # Tool 1: Web Search
    search = DuckDuckGoSearchRun()
    search_tool = Tool(
        name="web_search",
        func=search.run,
        description="Search the web for current or time-sensitive information. Use this for recent events, news, statistics, or anything that changes over time."
    )

    # Tool 2: Wikipedia
    wiki_wrapper = WikipediaAPIWrapper(top_k_results=2, doc_content_chars_max=2000)
    wiki = WikipediaQueryRun(api_wrapper=wiki_wrapper)
    wiki_tool = Tool(
        name="wikipedia",
        func=wiki.run,
        description="Look up factual and historical information from Wikipedia. Use this for well-established topics, definitions, biographies, and background knowledge."
    )

    # Tool 3: Summarize
    llm = ChatOllama(model=MODEL_NAME, base_url=OLLAMA_BASE_URL)

    def summarize_text(text):
        response = llm.invoke(f"Summarize the following text in 3-5 key bullet points:\n\n{text}")
        return response.content

    summarize_tool = Tool(
        name="summarize",
        func=summarize_text,
        description="Summarize a long piece of text into key bullet points. Use this when you have gathered a lot of information and need to condense it."
    )

    return [search_tool, wiki_tool, summarize_tool]