from app.rag.retrieval_service import (
    RetrievalService
)


def main():

    print()

    print(
        "🔎 NEXUS AI RETRIEVAL TEST"
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


    print()

    print(

        "🔎 Searching relevant documents..."

    )


    # ====================================================
    # SEARCH
    # ====================================================

    results = (

        retrieval_service

        .search(

            query

        )

    )


    # ====================================================
    # DISPLAY RESULTS
    # ====================================================

    if not results:

        print()

        print(

            "⚠️ No relevant documents found."

        )

        return


    print()

    print(

        f"📚 Found {len(results)} relevant results."

    )


    print()

    print(

        "=" * 60

    )


    for index, result in enumerate(

        results,

        start=1

    ):

        print()

        print(

            f"🔹 RESULT {index}"

        )

        print(

            "-" * 60

        )


        print(

            "🆔 Vector ID:",

            result[

                "vector_id"

            ]

        )


        print()

        print(

            "📝 Text:"

        )


        print(

            result[

                "text"

            ]

        )


        print()

        print(

            "📊 Distance:",

            result.get(

                "distance",

                "N/A"

            )

        )


        print()

        print(

            "📌 Metadata:",

            result[

                "metadata"

            ]

        )


        print()

        print(

            "-" * 60

        )


if __name__ == "__main__":

    main()