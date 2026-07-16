from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain_groq import ChatGroq
import os

from tools import web_search, scrape_url

load_dotenv()


llm = ChatGroq(
    
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile",
    temperature=0,
    max_tokens=4096
)


def build_search_agent():

    return create_agent(
        model=llm,
        tools=[web_search],
        system_prompt="""
You are a web research assistant.

Always use the web_search tool.

Return search results with URLs.
"""
    )


def build_reader_agent():

    return create_agent(
        model=llm,
        tools=[scrape_url],
        system_prompt="""
You are a webpage reader.

Your job:

1. Find the BEST URL inside the user message.
2. Call scrape_url(url)
3. Return ONLY the scraped content.

Always use the scrape_url tool.
"""
    )


writer_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an expert research writer.
Write detailed reports with headings.

Always include:

Introduction

Key Findings

Conclusion

Sources
"""
        ),
        (
            "human",
            """
Topic:
{topic}

Research:

{research}
"""
        )
    ]
)

writer_chain = writer_prompt | llm | StrOutputParser()


critic_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a research reviewer.
"""
        ),
        (
            "human",
            """
Review this report.

{report}

Return

Score

Strengths

Weaknesses

Suggestions
"""
        )
    ]
)

critic_chain = critic_prompt | llm | StrOutputParser()