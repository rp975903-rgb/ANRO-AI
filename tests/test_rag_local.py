from app.ai.llm.local_llm import LocalLLM

from app.rag.rag_service import (
    RAGService
)


def print_separator():
    print("=" * 70)


def main():

    print_separator()

    print(
        "🧠 NEXUS AI END-TO-END RAG TEST"
    )

    print_separator()


    # ========================================================
    # INITIALIZE LOCAL LLM
    # ========================================================

    print(
        "\n🤖 Initializing Local LLM..."
    )


    llm = LocalLLM(

        model_name="nexus-local-test"

    )


    print(

        f"✅ LLM Ready: "
        f"{llm.model_name}"

    )


    # ========================================================
    # INITIALIZE RAG SERVICE
    # ========================================================

    print(
        "\n🧠 Initializing RAG Service..."
    )


    rag_service = RAGService(

        llm=llm,

        conversation_id=
            "test_conversation",

        top_k=3,

        max_context_length=5000

    )


    print(
        "✅ RAG Service Ready"
    )


    # ========================================================
    # TEST QUESTIONS
    # ========================================================

    questions = [

        "What is Python?",

        "What is Python used for?",

        "What are its main applications?"

    ]


    # ========================================================
    # ASK QUESTIONS
    # ========================================================

    for index, question in enumerate(

        questions,

        start=1

    ):

        print_separator()

        print(

            f"👤 QUESTION {index}:"

        )

        print(

            question

        )


        try:

            result = (

                rag_service

                .ask(

                    question

                )

            )


            # =================================================
            # DISPLAY ANSWER
            # =================================================

            print(

                "\n🤖 ANSWER:"

            )

            print(

                result.get(

                    "answer",

                    "No answer generated."

                )

            )


            # =================================================
            # DISPLAY REWRITTEN QUERY
            # =================================================

            print(

                "\n🔄 REWRITTEN QUERY:"

            )

            print(

                result.get(

                    "rewritten_query",

                    "N/A"

                )

            )


            # =================================================
            # DISPLAY RETRIEVAL ANALYSIS
            # =================================================

            analysis = (

                result.get(

                    "analysis",

                    {}

                )

            )


            print(

                "\n📊 RETRIEVAL ANALYSIS:"

            )


            print(

                f"Confidence Score: "
                f"{analysis.get('confidence_score')}"

            )


            print(

                f"Confidence Level: "
                f"{analysis.get('confidence_level')}"

            )


            print(

                f"Result Count: "
                f"{analysis.get('result_count')}"

            )


            print(

                f"Best Distance: "
                f"{analysis.get('best_distance')}"

            )


            # =================================================
            # DISPLAY CITATIONS
            # =================================================

            print(

                "\n📚 SOURCE CITATIONS:"

            )


            citations = (

                result.get(

                    "citations",

                    []

                )

            )


            if citations:

                for citation in citations:

                    print(

                        citation

                    )

            else:

                print(

                    "No citations available."

                )


            # =================================================
            # MEMORY INFORMATION
            # =================================================

            print(

                "\n🧠 CONVERSATION MEMORY:"

            )


            print(

                f"Conversation ID: "

                f"{result.get('conversation_id')}"

            )


            print(

                f"Memory Size: "

                f"{result.get('memory_size')}"

            )


            print(

                "\n✅ Question processed successfully."

            )


        except Exception as error:

            print(

                "\n❌ RAG ERROR:"

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

    print_separator()

    print(

        "🎉 NEXUS AI RAG TEST COMPLETE"

    )

    print_separator()


if __name__ == "__main__":

    main()