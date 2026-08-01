from app.document_processing.document_loader_factory import (
    DocumentLoaderFactory
)


def main():

    print()

    print(
        "📚 NEXUS AI DOCUMENT LOADER FACTORY TEST"
    )

    print(
        "=" * 60
    )


    test_files = [

        "data/documents/sample.txt",

        "data/documents/sample.pdf",

        "data/documents/sample.docx",

    ]


    for file_path in test_files:

        print()

        print(
            "📄 File:",
            file_path
        )


        try:

            loader = (

                DocumentLoaderFactory

                .get_loader(

                    file_path

                )

            )


            print(

                "🔧 Loader:",

                type(loader).__name__

            )


            text = (

                loader

                .load(

                    file_path

                )

            )


            print(

                "📝 Extracted Characters:",

                len(text)

            )


            if text.strip():

                print(

                    "✅ Text Extraction Successful"

                )

            else:

                print(

                    "⚠️ No Text Found"

                )


        except Exception as error:

            print()

            print(

                "❌ ERROR:",

                error

            )


if __name__ == "__main__":

    main()