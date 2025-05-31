import os

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from .shared_prompts import POST_STYLE

llm = ChatOpenAI(model=os.environ["SMALL_MODEL"])


class ReviewResult(BaseModel):
    acceptable: bool = Field(
        description="True if the provided blog post draft is acceptable for publication, or false if it needs a rewrite."
    )


structured_llm_reviewer = llm.with_structured_output(ReviewResult)
system = """You are the reviewer of a blog post draft.\n
    Your task is to determine whether the draft is acceptable for publication or if it needs a rewrite.\n
    If the draft contains sufficient information and is well-written, return true.\n
    If the draft is missing information, indicates that sections are incomplete or need more knowledge to write, or it is simply poorly written, return false."""
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("system", POST_STYLE),
        ("human", "Blog post draft: \n\n {post_content}"),
    ]
)

reviewer_chain = prompt | structured_llm_reviewer
