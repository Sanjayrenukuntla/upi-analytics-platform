
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter

from ai.config import (
    KNOWLEDGE_BASE_DIR,
    VECTOR_STORE_DIR,
    COLLECTION_NAME,
    EMBEDDING_MODEL_NAME,
)


def ingest_documents():

    if not KNOWLEDGE_BASE_DIR.exists():
        raise FileNotFoundError(
            f"Knowledge base folder not found: {KNOWLEDGE_BASE_DIR}"
        )

    files = list(KNOWLEDGE_BASE_DIR.glob("*.txt"))

    if not files:
        raise FileNotFoundError(
            "No .txt files found in the knowledge_base folder."
        )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    embedding_model = SentenceTransformer(
        EMBEDDING_MODEL_NAME
    )

    VECTOR_STORE_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    client = chromadb.PersistentClient(
        path=str(VECTOR_STORE_DIR)
    )

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    documents = []
    metadatas = []
    ids = []

    for file_path in files:

        text = file_path.read_text(
            encoding="utf-8"
        )

        chunks = splitter.split_text(text)

        for index, chunk in enumerate(chunks):

            documents.append(chunk)

            metadatas.append({
                "source": file_path.name
            })

            ids.append(
                f"{file_path.stem}_{index}"
            )

    embeddings = embedding_model.encode(
        documents,
        show_progress_bar=True
    ).tolist()

    collection.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings
    )

    print(
        f"Successfully stored {len(documents)} chunks "
        f"from {len(files)} document(s)."
    )


if __name__ == "__main__":
    ingest_documents()
