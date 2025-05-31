import os

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from .shared_prompts import POST_STYLE


llm = ChatOpenAI(model=os.environ["LARGE_MODEL"])

job_description = """You are an experienced blog writer tasked with writing a blog post on a given topic to be published to a software engineering and solution architect blog.\n
    A researcher has already performed search queries on relevant information and provided you with all the knowledge they found.\n
    Given the requested topic and existing knowledge, write a comprehensive blog post that is engaging and informative.\n
    An outline is provided for you to write the blog post and you must stick to this outline unless it is vital to alter it to make the post flow better.\n
    If this is not the first time the blog has been drafted, a previous draft is also provided along with feedback about the draft from the user.\n
    Do not use any of your own knowledge to generate the blog post; if the given knowledge is insufficient to write a compelling post, clearly define the topics that will need more research at the start of the post and the researcher will do more research.\n
    The blog post should be suitable for a reader with limited background knowledge on the topic.\n
    The post should stay under 10 minutes of reading time and should be written in Markdown format."""

with open("graph/chains/existing_post.md", "r") as file:
    existing_post = file.read()

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", job_description),
        ("system", POST_STYLE),
        (
            "system",
            "What follows is an example of a blog post that matches the style.\n\n"
            + existing_post,
        ),
        ("human", "Requested blog topic:\n\n{request}"),
        ("human", "Knowledge:\n\n{knowledge}"),
        ("human", "Outline:\n\n{outline}"),
        ("human", "Previous draft:\n\n{previous_draft}"),
        ("human", "User feedback on previous draft:\n\n{user_feedback}"),
    ]
)

writer_chain = prompt | llm | StrOutputParser()
