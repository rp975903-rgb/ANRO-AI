from app.ai.llm.mock_llm import (
    MockLLM
)

from app.rag.rag_service import (
    RAGService
)


def main():

    print()

    print(
        "🧠 NEXUS AI RAG SYSTEM TEST"
    )

    print(
        "=" * 60
    )


    # ====================================================
    # CREATE LLM
    # ====================================================

    llm = MockLLM()


    # ====================================================
    # CREATE RAG SERVICE
    # ====================================================

    rag_service = RAGService(

        llm=llm,

        top_k=3,

        max_context_length=5000

    )


    # ====================================================
    # USER QUESTION
    # ====================================================

    question = (

        "What is Python?"

    )


    print()

    print(
        "👤 QUESTION:"
    )

    print(
        question
    )


    # ====================================================
    # ASK RAG SYSTEM
    # ====================================================

    result = (

        rag_service

        .ask(

            question

        )

    )


    # ====================================================
    # DISPLAY ANSWER
    # ====================================================

    print()

    print(
        "🤖 ANSWER"
    )

    print(
        "-" * 60
    )

    print(
        result["answer"]
    )


    # ====================================================
    # DISPLAY RETRIEVAL ANALYSIS
    # ====================================================

    print()

    print(
        "📊 RETRIEVAL ANALYSIS"
    )

    print(
        "-" * 60
    )


    analysis = result["analysis"]


    print(

        "Confidence Score:",

        analysis[
            "confidence_score"
        ]

    )


    print(

        "Confidence Level:",

        analysis[
            "confidence_level"
        ]

    )


    print(

        "Best Distance:",

        analysis[
            "best_distance"
        ]

    )


    print(

        "Average Distance:",

        analysis[
            "average_distance"
        ]

    )


    print(

        "Results Found:",

        analysis[
            "result_count"
        ]

    )


    # ====================================================
    # DISPLAY SOURCE CITATIONS
    # ====================================================

    print()

    print(
        "📚 SOURCE CITATIONS"
    )

    print(
        "-" * 60
    )


    citations = result["citations"]


    if not citations:

        print(
            "⚠️ No source citations found."
        )


    else:

        for citation in citations:

            print()

            print(

                f"📌 Source "
                f"{citation['source_number']}"

            )


            print(

                "Document ID:",

                citation[
                    "document_id"
                ]

            )


            print(

                "Chunk:",

                citation[
                    "chunk_index"
                ]

            )


            print(

                "Distance:",

                citation[
                    "distance"
                ]

            )


            print(

                "Preview:",

                citation[
                    "preview"
                ]

            )


    # ====================================================
    # DISPLAY RAG CONTEXT
    # ====================================================

    print()

    print(
        "📖 RAG CONTEXT"
    )

    print(
        "-" * 60
    )


    context = result["context"]


    if context:

        print(
            context
        )

    else:

        print(
            "⚠️ No context generated."
        )


    # ====================================================
    # TEST COMPLETE
    # ====================================================

    print()

    print(
        "=" * 60
    )

    print(
        "✅ NEXUS AI RAG TEST COMPLETED"
    )

    print(
        "=" * 60
    )


if __name__ == "__main__":

    main()