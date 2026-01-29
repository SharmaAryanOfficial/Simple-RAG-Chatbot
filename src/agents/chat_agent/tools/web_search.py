from langchain_community.tools import DuckDuckGoSearchRun
from langchain.tools import tool

search = DuckDuckGoSearchRun()

@tool
def search_the_web (query : str) ->str:
    """
    Docstring for search_the_web
    
    use this tool to search the web
    :param query: Description
    :type query: str
    :return: Description
    :rtype: str
    """

    return search.invoke(query)