from app.rag.query_rewriter import (
    QueryRewriter
)


def main():

    print()

    print(
        "🔄 NEXUS AI QUERY REWRITER TEST"
    )

    print(
        "=" * 60
    )


    # ====================================================
    # CREATE REWRITER
    # ====================================================

    rewriter = QueryRewriter()


    # ====================================================
    # CONVERSATION HISTORY
    # ====================================================

    conversation_history = [

        {

            "role":
                "user",

            "content":
                "What is Python?"

        },

        {

            "role":
                "assistant",

            "content":
                "Python is a programming language."

        },

    ]


    # ====================================================
    # FOLLOW-UP QUESTION
    # ====================================================

    question = (

        "What is it used for?"

    )


    print()

    print(
        "👤 Original Question:"
    )

    print(
        question
    )


    # ====================================================
    # REWRITE
    # ====================================================

    rewritten_query = (

        rewriter.rewrite(

            question,

            conversation_history

        )

    )


    print()

    print(
        "🔄 Rewritten Query:"
    )

    print(
        rewritten_query
    )


    # ====================================================
    # TEST NEW QUESTION
    # ====================================================

    new_question = (

        "Explain machine learning."

    )


    new_query = (

        rewriter.rewrite(

            new_question,

            conversation_history

        )

    )


    print()

    print(
        "👤 New Question:"
    )

    print(
        new_question
    )


    print()

    print(
        "🔄 Rewritten Query:"
    )

    print(
        new_query
    )


    print()

    print(
        "✅ QUERY REWRITER TEST COMPLETED"
    )


if __name__ == "__main__":

    main()