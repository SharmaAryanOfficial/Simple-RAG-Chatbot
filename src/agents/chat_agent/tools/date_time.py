import time
from langchain.tools import tool

@tool
def get_current_date_and_time() -> str:
    """
    Docstring for get_current_date_and_time

    Use this to get current date and time.
    
    :return: Description
    :rtype: str
    """
    return time.ctime()