import os

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field


llm = ChatOpenAI(model = os.environ["MODEL"])


class ResearchResult(BaseModel):
    search_queries: list[str] = Field(
        description="List of search queries to make to find information relevant to the blog post topic."
    )


structured_llm_researcher = llm.with_structured_output(ResearchResult)
system = """You are a researcher tasked with generating search queries to find information relevant to a blog post topic. \n
    Given a user request, generate a list of search queries that will help gather information to write a blog post on that topic. \n
    The search queries should be concise and relevant to the topic at hand. \n
    You should also consider the existing knowledge provided to avoid redundant searches. \n
    The results need to be comprehensive for the topic, allowing a blog post to be written that will allow readers with limited background knowledge to understand the topic. \n
    Limit the number of search queries to 3. \n"""
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "Requested blog topic: \n\n {request} \n\n Existing knowledge: {knowledge}"),
    ]
)

research_chain = prompt | structured_llm_researcher
