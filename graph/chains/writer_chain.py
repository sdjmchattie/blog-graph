import os

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from .shared_prompts import POST_STYLE


llm = ChatOpenAI(model = os.environ["MODEL"])

job_description = """You are an experienced blog writer tasked with writing a blog post on a given topic to be published to a software engineering and solution architect blog.\n
    A researcher has already performed search queries on relevant information and provided you with all the knowledge they found.\n
    Given the requested topic and existing knowledge, write a comprehensive blog post that is engaging and informative.\n
    If this is not the first time the blog has been drafted, a previous draft is also provided as a reference for improvements.\n
    The blog post should be suitable for a reader with limited background knowledge on the topic.\n
    The post should stay under 10 minutes of reading time and should be written in Markdown format.\n
    If the knowledge is not sufficient to write a blog post, be explicit in your draft about where more information would allow the post to be better written."""

with open('graph/chains/existing_post.md', 'r') as file:
    existing_post = file.read()

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", job_description),
        ("system", POST_STYLE),
        ("system", "What follows is an example of a blog post that matches the style.\n\n" + existing_post),
        ("human", "Requested blog topic: \n\n {request} \n\n Knowledge: {knowledge} \n\n Previous draft: \n\n {previous_draft}"),
    ]
)

writer_chain = prompt | llm | StrOutputParser()
