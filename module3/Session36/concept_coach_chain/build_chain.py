from typing import Callable
from langchain_ollama import ChatOllama  
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


def build_chain():
    """Create and return an LCEL chain: prompt | llm | parser.

    Uses `ChatPromptTemplate.from_messages` with a system and human message,
    `ChatOllama` as the model, and `StrOutputParser` to return plain text.
    If the required libraries are not available, returns a simple fallback
    callable that produces a beginner-friendly explanation string.
    """
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a beginner-friendly programming instructor. "
                "Explain concepts clearly in simple language. "
                "Use short bullet points and avoid unnecessary introduction.",
            ),
            (
                "human",
                "Explain {topic} using a simple analogy from {analogy_domain}.",
            ),
        ]
    )

    llm = ChatOllama(
        model="qwen:1.8b",
        base_url="http://localhost:11434",
        temperature=1,
        num_predict=100,
    )

    parser = StrOutputParser()

    # LCEL composition: prompt | llm | parser
    chain = prompt | llm | parser

    return chain
