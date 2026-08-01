from app.document_processing.document_ingestion_service import (
    DocumentIngestionService
)


def main():

    print()

    print(
        "🧠 NEXUS AI DOCUMENT INGESTION TEST"
    )

    print(
        "=" * 60
    )


    service = (

        DocumentIngestionService()

    )


    test_files = [

        "data/documents/sample.txt",

        "data/documents/sample.pdf",

        "data/documents/sample.docx",

    ]


    for file_path in test_files:

        print()

        print(

            f"📄 Processing: "
            f"{file_path}"

        )


        try:

            result = (

                service

                .ingest_document(

                    file_path

                )

            )


            print()

            print(

                "✅ INGESTION SUCCESSFUL"

            )


            print(

                "Document ID:",

                result["document_id"]

            )


            print(

                "Filename:",

                result["filename"]

            )


            print(

                "File Type:",

                result["file_type"]

            )


            print(

                "Total Chunks:",

                result["total_chunks"]

            )


            print(

                "Vector IDs:",

                len(

                    result["vector_ids"]

                )

            )


            print(

                "Status:",

                result["status"]

            )


        except Exception as error:

            print()

            print(

                "❌ INGESTION FAILED"

            )


            print(

                "Error:",

                error

            )


if __name__ == "__main__":

    main()