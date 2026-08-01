from app.document_processing.document_ingestion_service import (
    DocumentIngestionService
)


def main():

    print()

    print(
        "🚀 NEXUS AI DOCUMENT INGESTION TEST"
    )

    print(
        "=" * 60
    )


    # ====================================================
    # CREATE INGESTION SERVICE
    # ====================================================

    ingestion_service = (

        DocumentIngestionService()

    )


    # ====================================================
    # DOCUMENT PATH
    # ====================================================

    document_path = (

        "data/documents/sample.txt"

    )


    print()

    print(

        "📄 Processing Document:"

    )

    print(

        document_path

    )


    # ====================================================
    # INGEST DOCUMENT
    # ====================================================

    result = (

        ingestion_service

        .ingest_document(

            document_path

        )

    )


    # ====================================================
    # DISPLAY RESULT
    # ====================================================

    print()

    print(

        "✅ DOCUMENT INGESTED SUCCESSFULLY"

    )


    print()

    print(

        "🆔 Document ID:"

    )

    print(

        result[

            "document_id"

        ]

    )


    print()

    print(

        "📄 Filename:"

    )

    print(

        result[

            "filename"

        ]

    )


    print()

    print(

        "🧩 Total Chunks:"

    )

    print(

        result[

            "total_chunks"

        ]

    )


    print()

    print(

        "💾 Vector IDs:"

    )


    for vector_id in result[

        "vector_ids"

    ]:

        print(

            vector_id

        )


    print()

    print(

        "📊 Status:"

    )

    print(

        result[

            "status"

        ]

    )


if __name__ == "__main__":

    main()