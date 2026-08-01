from app.rag.retrieval_service import (
    RetrievalService
)

from app.rag.context_builder import (
    RAGContextBuilder
)


def main():

    print()

    print(
        "🧠 NEXUS AI RAG CONTEXT BUILDER TEST"
    )

    print(
        "=" * 60
    )


    # ====================================================
    # CREATE RETRIEVAL SERVICE
    # ====================================================

    retrieval_service = (

        RetrievalService(

            top_k=3

        )

    )


    # ====================================================
    # CREATE CONTEXT BUILDER
    # ====================================================

    context_builder = (

        RAGContextBuilder(

            max_context_length=5000

        )

    )


    # ====================================================
    # USER QUERY
    # ====================================================

    query = (

        "What is Python?"

    )


    print()

    print(

        "👤 Query:",

        query

    )


    # ====================================================
    # RETRIEVE DOCUMENTS
    # ====================================================

    results = (

        retrieval_service

        .search(

            query

        )

    )


    if not results:

        print()

        print(

            "⚠️ No relevant documents found."

        )

        return


    # ====================================================
    # BUILD RAG CONTEXT
    # ====================================================

    context = (

        context_builder

        .build_context(

            results

        )

    )


    # ====================================================
    # DISPLAY CONTEXT
    # ====================================================

    print()

    print(

        "📚 GENERATED RAG CONTEXT"

    )

    print(

        "-" * 60

    )


    print(

        context

    )


    # ====================================================
    # CONTEXT STATISTICS
    # ====================================================

    statistics = (

        context_builder

        .get_context_statistics(

            context

        )

    )


    print()

    print(

        "📊 CONTEXT STATISTICS"

    )

    print(

        "-" * 60

    )


    print(

        "Characters:",

        statistics[

            "characters"

        ]

    )


    print(

        "Words:",

        statistics[

            "words"

        ]

    )


    print(

        "Sources:",

        statistics[

            "sources"

        ]

    )


if __name__ == "__main__":

    main()