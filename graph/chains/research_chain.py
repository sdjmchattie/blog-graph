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
    Given the requested topic and existing knowledge generate a list of search queries to complete the research on the topic. \n
    The knowledge needs to be comprehensive enough to write a blog post for a reader with limited background knowledge. \n
    Only suggest at most 3 searches. \n
    Be conservative and suggest no searches if the knowledge is already good enough."""
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "Requested blog topic: \n\n {request} \n\n Existing knowledge: {knowledge}"),
    ]
)

research_chain = prompt | structured_llm_researcher
