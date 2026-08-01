from app.document_processing.document_ingestion_manager import (
    DocumentIngestionManager
)


def main():

    print()
    print("=" * 70)
    print("📚 NEXUS AI DOCUMENT INGESTION MANAGER TEST")
    print("=" * 70)

    manager = (
        DocumentIngestionManager(
            chunk_size=500,
            chunk_overlap=50
        )
    )

    print()
    print(
        "Supported Extensions:",
        manager.get_supported_extensions()
    )

    documents_directory = (
        "data/documents"
    )

    print()
    print(
        f"📂 Processing Directory: "
        f"{documents_directory}"
    )

    results = (
        manager.ingest_directory(
            documents_directory
        )
    )

    print()
    print("=" * 70)
    print("📊 INGESTION RESULTS")
    print("=" * 70)

    for result in results:

        print()

        print(
            f"📄 File: "
            f"{result.get('filename')}"
        )

        print(
            f"Status: "
            f"{result.get('status')}"
        )

        if (
            result.get("status")
            == "processed"
        ):

            print(
                f"Document ID: "
                f"{result.get('document_id')}"
            )

            print(
                f"Characters: "
                f"{result.get('characters')}"
            )

            print(
                f"Chunks: "
                f"{result.get('total_chunks')}"
            )

        else:

            print(
                f"❌ Error: "
                f"{result.get('error')}"
            )

    print()
    print("=" * 70)
    print("✅ INGESTION MANAGER TEST COMPLETE")
    print("=" * 70)


if __name__ == "__main__":

    main()