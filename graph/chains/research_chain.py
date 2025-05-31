import os

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field


llm = ChatOpenAI(model=os.environ["SMALL_MODEL"])


class ResearchResult(BaseModel):
    search_queries: list[str] = Field(
        description="List of search queries to make to find information relevant to the blog post topic."
    )


structured_llm_researcher = llm.with_structured_output(ResearchResult)
system = """You are a researcher tasked with generating search queries to find information relevant to a described blog post.\n
    Given the requested topic and existing knowledge generate a list of search queries to complete the research on the topic.\n
    The research should allow the given outline to be fully populated with information.\n
    If a previous draft was done, it has been provided to you along with the user's feedback on the draft.\n
    The knowledge needs to be comprehensive enough to write a blog post for a reader with limited background knowledge.\n
    Only suggest at most 5 searches."""
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "Requested blog topic:\n\n{request}"),
        ("human", "Existing knowledge:\n\n{knowledge}"),
        ("human", "Outline:\n\n{outline}"),
        ("human", "Previous draft:\n\n{blog_draft}"),
        ("human", "User feedback on the latest draft:\n\n{user_feedback}"),
    ]
)

research_chain = prompt | structured_llm_researcher
