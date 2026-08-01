from app.ai.embedding_service import EmbeddingService


def main():

    print(
        "🧠 NEXUS AI EMBEDDING TEST"
    )

    print(
        "-" * 60
    )


    embedding_service = (

        EmbeddingService()

    )


    text = (

        "Python is a powerful "
        "programming language."

    )


    print()

    print(
        "📝 Input Text:"
    )

    print(
        text
    )


    embedding = (

        embedding_service

        .generate_embedding(

            text

        )

    )


    print()

    print(
        "🔢 Embedding Type:"
    )

    print(
        type(

            embedding

        )

    )


    print()

    print(
        "📏 Embedding Dimension:"
    )

    print(

        len(

            embedding

        )

    )


    print()

    print(
        "🔢 First 10 Values:"
    )

    print(

        embedding[:10]

    )


if __name__ == "__main__":

    main()