import os

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model=os.environ["SMALL_MODEL"])

system = """You are a blog post specialist.\n
    You must take the requested blog topic and prepare an outline for the post.\n
    If the user has already seen an outline, there will be user feedback which you should follow closely when generating a new outline.\n
    When there is user feedback, the previous outline is also provided.\n
    Generate nothing but the new outline, in Markdown format, with no additional text.\n
    The outline must use level 2 and level 3 headings only.\n
    All spellings must be in UK English.\n
    After each heading, an insertion marker with a super brief summary should be placed.\n
    Before the first heading, put an insertion marker for a short punchy introduction.\n
    The last header must always be a level 2 header with the title "Wrapping Up".\n"""
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "Requested blog topic:\n\n{request}"),
        ("human", "My feedback on the previous outline:\n\n{user_feedback}"),
        ("human", "The previous outline:\n\n{outline}"),
    ]
)

outline_chain = prompt | llm | StrOutputParser()
