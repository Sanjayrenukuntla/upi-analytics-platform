
import time
from functools import lru_cache

import chromadb
from sentence_transformers import SentenceTransformer
from google import genai

from ai.config import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
    TOP_K,
    COLLECTION_NAME,
    EMBEDDING_MODEL_NAME,
    VECTOR_STORE_DIR,
)

from ai.analytics_tools import get_analytics_context


# --------------------------------------------------
# 1. CACHED RESOURCES
# --------------------------------------------------

@lru_cache(maxsize=1)
def get_embedding_model():
    """Load the embedding model only once."""

    return SentenceTransformer(
        EMBEDDING_MODEL_NAME
    )


@lru_cache(maxsize=1)
def get_chroma_collection():
    """Create the database connection only once."""

    client = chromadb.PersistentClient(
        path=str(VECTOR_STORE_DIR)
    )

    return client.get_collection(
        name=COLLECTION_NAME
    )


@lru_cache(maxsize=1)
def get_gemini_client():
    """Create the Gemini client only once."""

    if not GEMINI_API_KEY:
        raise ValueError(
            "Gemini API key not found. "
            "Check the .env file in the project root."
        )

    return genai.Client(
        api_key=GEMINI_API_KEY
    )


# --------------------------------------------------
# 2. RETRIEVE CONTEXT
# --------------------------------------------------

def retrieve_context(question, top_k=TOP_K):

    model = get_embedding_model()
    collection = get_chroma_collection()

    embedding = model.encode(
        question
    ).tolist()

    results = collection.query(
        query_embeddings=[embedding],
        n_results=top_k
    )

    documents = results.get(
        "documents", [[]]
    )[0]

    metadatas = results.get(
        "metadatas", [[]]
    )[0]

    retrieved = []

    for document, metadata in zip(
        documents, metadatas
    ):

        retrieved.append({
            "content": document,
            "source": metadata.get(
                "source", "Unknown"
            )
        })

    return retrieved


# --------------------------------------------------
# 3. BUILD PROMPT
# --------------------------------------------------

def build_prompt(question, retrieved_context):

    knowledge = "\n\n".join(
        [
            f"Source: {item['source']}\n"
            f"{item['content']}"
            for item in retrieved_context
        ]
    )

    try:
        analytics = get_analytics_context()
    except Exception as error:
        analytics = (
            "Dataset analytics are currently unavailable: "
            f"{error}"
        )

    return f"""
You are the AI assistant for UPI Pulse,
an Indian digital payments analytics platform.

Answer the user's question clearly and accurately.

RULES:
1. Use the supplied project knowledge and dataset analytics.
2. Never invent statistics or findings.
3. If information is unavailable, say so.
4. Distinguish calculated dataset figures from general explanations.
5. Explain technical topics in simple language.
6. Mention limitations when relevant.

PROJECT KNOWLEDGE:
{knowledge}

DATASET ANALYTICS:
{analytics}

USER QUESTION:
{question}

ANSWER:
"""


# --------------------------------------------------
# 4. GEMINI RESPONSE
# --------------------------------------------------

def generate_answer(prompt, max_retries=3):

    client = get_gemini_client()

    for attempt in range(max_retries):

        try:

            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt
            )

            if not response.text:
                raise RuntimeError(
                    "Gemini returned an empty response."
                )

            return response.text

        except Exception as error:

            message = str(error).lower()

            temporary = any(
                term in message
                for term in [
                    "429",
                    "500",
                    "502",
                    "503",
                    "504",
                    "unavailable",
                    "resource exhausted",
                    "timeout"
                ]
            )

            if not temporary:
                raise RuntimeError(
                    f"Gemini API error: {error}"
                ) from error

            if attempt == max_retries - 1:
                raise RuntimeError(
                    "Gemini is temporarily unavailable. "
                    "Please try again later."
                ) from error

            time.sleep(2 ** attempt)


# --------------------------------------------------
# 5. MAIN RAG FUNCTION
# --------------------------------------------------

def answer_question(question):

    if not question or not question.strip():
        return "Please enter a question."

    retrieved_context = retrieve_context(question)

    if not retrieved_context:
        return (
            "I couldn't find relevant information "
            "in the UPI Pulse knowledge base."
        )

    prompt = build_prompt(
        question,
        retrieved_context
    )

    return generate_answer(prompt)
