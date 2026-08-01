from app.ai.embedding_service import EmbeddingService

from app.vector_store.chroma_store import (
    ChromaVectorStore
)


def main():

    print(

        "🗄️ NEXUS AI VECTOR STORE TEST"

    )

    print(

        "-" * 60

    )


    # ====================================================
    # CREATE SERVICES
    # ====================================================

    embedding_service = (

        EmbeddingService()

    )


    vector_store = (

        ChromaVectorStore()

    )


    # ====================================================
    # SAMPLE DOCUMENT
    # ====================================================

    document_id = (

        "test_document_001"

    )


    chunks = [

        "Python is a powerful programming language.",

        "Machine learning uses algorithms to learn from data.",

        "Natural Language Processing helps computers understand human language."

    ]


    print()

    print(

        "📄 Number of Chunks:"

    )

    print(

        len(chunks)

    )


    # ====================================================
    # GENERATE EMBEDDINGS
    # ====================================================

    embeddings = (

        embedding_service

        .generate_embeddings(

            chunks

        )

    )


    print()

    print(

        "🧠 Embeddings Generated:"

    )

    print(

        len(embeddings)

    )


    # ====================================================
    # STORE VECTORS
    # ====================================================

    ids = (

        vector_store

        .add_chunks(

            document_id,

            chunks,

            embeddings

        )

    )


    print()

    print(

        "💾 Stored Vector IDs:"

    )


    for vector_id in ids:

        print(

            vector_id

        )


    # ====================================================
    # COUNT VECTORS
    # ====================================================

    print()

    print(

        "📊 Total Stored Vectors:"

    )

    print(

        vector_store.count()

    )


    # ====================================================
    # SEMANTIC SEARCH
    # ====================================================

    query = (

        "What is Python?"

    )


    query_embedding = (

        embedding_service

        .generate_embedding(

            query

        )

    )


    results = (

        vector_store

        .search(

            query_embedding,

            top_k=2

        )

    )


    print()

    print(

        "🔎 SEARCH QUERY:"

    )

    print(

        query

    )


    print()

    print(

        "🎯 MOST RELEVANT CHUNKS:"

    )


    for document in results[

        "documents"

    ][0]:

        print()

        print(

            "➡️",

            document

        )


if __name__ == "__main__":

    main()