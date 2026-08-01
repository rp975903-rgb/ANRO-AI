from app.services.document_search_service import (
    DocumentSearchService
)


def main():

    print("=" * 70)

    print(
        "🔎 NEXUS AI DOCUMENT SEARCH SERVICE TEST"
    )

    print("=" * 70)


    # ========================================================
    # INITIALIZE SERVICE
    # ========================================================

    print(
        "\n🧠 Initializing Document Search Service..."
    )


    service = DocumentSearchService(

        top_k=5

    )


    print(
        "✅ Document Search Service Ready"
    )


    # ========================================================
    # SERVICE STATUS
    # ========================================================

    print(
        "\n📊 SERVICE STATUS"
    )


    status = (

        service

        .get_status()

    )


    print(

        f"Status: "
        f"{status['status']}"

    )


    print(

        f"Collection: "
        f"{status['collection_name']}"

    )


    print(

        f"Total Chunks: "
        f"{status['total_chunks']}"

    )


    # ========================================================
    # SEARCH DOCUMENTS
    # ========================================================

    query = (

        "What is Python?"

    )


    print(
        "\n🔍 SEARCH QUERY:"
    )


    print(
        query
    )


    try:

        results = (

            service

            .search(

                query=query,

                top_k=5

            )

        )


        # ====================================================
        # DISPLAY RESULTS
        # ====================================================

        print(
            "\n📚 SEARCH RESULTS"
        )


        if not results:

            print(
                "No matching documents found."
            )


        else:

            for result in results:

                print(
                    "\n----------------------------------------"
                )


                print(

                    f"Rank: "
                    f"{result['rank']}"

                )


                print(

                    f"Vector ID: "
                    f"{result['vector_id']}"

                )


                print(

                    f"Distance: "
                    f"{result['distance']}"

                )


                print(

                    f"Text:\n"
                    f"{result['text']}"

                )


                print(

                    f"Metadata: "
                    f"{result['metadata']}"

                )


        print(
            "\n✅ Search test completed successfully."
        )


    except Exception as error:

        print(
            "\n❌ SEARCH ERROR:"
        )


        print(
            type(error).__name__
        )


        print(
            str(error)
        )


    # ========================================================
    # FINAL STATUS
    # ========================================================

    print("\n" + "=" * 70)

    print(
        "🎉 DOCUMENT SEARCH SERVICE TEST COMPLETE"
    )

    print("=" * 70)


if __name__ == "__main__":

    main()