from app.rag.rag_service import RAGService


class CLIChat:
    """
    Command Line Chat Interface
    for NEXUS AI.
    """

    def __init__(
        self,
        rag_service: RAGService
    ):
        self.rag_service = rag_service

    def display_header(self):
        print()
        print("=" * 70)
        print("                 🧠 NEXUS AI")
        print("          DOCUMENT INTELLIGENCE ASSISTANT")
        print("=" * 70)
        print()
        print("Ask questions about your documents.")
        print()
        print("Commands:")
        print("  /help   - Show available commands")
        print("  /stats  - Show conversation statistics")
        print("  /clear  - Clear conversation memory")
        print("  /exit   - Exit NEXUS AI")
        print()

    def display_help(self):
        print()
        print("-" * 70)
        print("📚 NEXUS AI COMMANDS")
        print("-" * 70)
        print()
        print("/help   → Show this help menu")
        print("/stats  → Show conversation statistics")
        print("/clear  → Clear current conversation")
        print("/exit   → Exit the application")
        print()

    def display_stats(
        self,
        result: dict
    ):
        print()
        print("-" * 70)
        print("📊 RAG ANALYSIS")
        print("-" * 70)

        analysis = result.get(
            "analysis",
            {}
        )

        print(
            f"Conversation ID: "
            f"{result.get('conversation_id', 'N/A')}"
        )

        print(
            f"Memory Size: "
            f"{result.get('memory_size', 0)}"
        )

        print(
            f"Retrieved Results: "
            f"{analysis.get('result_count', 0)}"
        )

        print(
            f"Confidence Score: "
            f"{analysis.get('confidence_score', 0)}"
        )

        print(
            f"Confidence Level: "
            f"{analysis.get('confidence_level', 'unknown')}"
        )

        print(
            f"Best Distance: "
            f"{analysis.get('best_distance', 'N/A')}"
        )

        print()

    def display_citations(
        self,
        citations
    ):
        if not citations:
            print()
            print("📚 Sources: No citations available.")
            return

        print()
        print("-" * 70)
        print("📚 SOURCE CITATIONS")
        print("-" * 70)

        for index, citation in enumerate(
            citations,
            start=1
        ):
            print(
                f"\n[{index}] {citation}"
            )

        print()

    def display_response(
        self,
        result: dict
    ):
        print()
        print("-" * 70)
        print("🤖 NEXUS AI")
        print("-" * 70)

        print()

        print(
            result.get(
                "answer",
                "No answer generated."
            )
        )

        print()

        self.display_stats(
            result
        )

        self.display_citations(
            result.get(
                "citations",
                []
            )
        )

    def start(self):
        """
        Start interactive CLI chat.
        """

        self.display_header()

        while True:

            try:

                question = input(
                    "\n👤 You: "
                ).strip()

            except KeyboardInterrupt:

                print(
                    "\n\n👋 Goodbye!"
                )

                break

            except EOFError:

                print(
                    "\n\n👋 Goodbye!"
                )

                break

            if not question:
                continue

            # =================================================
            # EXIT
            # =================================================

            if question.lower() in (
                "/exit",
                "exit",
                "quit"
            ):
                print()
                print(
                    "👋 Thank you for using NEXUS AI."
                )
                print(
                    "See you next time!"
                )
                break

            # =================================================
            # HELP
            # =================================================

            if question.lower() == "/help":

                self.display_help()

                continue

            # =================================================
            # CLEAR MEMORY
            # =================================================

            if question.lower() == "/clear":

                success = (
                    self.rag_service
                    .clear_conversation()
                )

                if success:

                    print()
                    print(
                        "🧹 Conversation memory cleared."
                    )

                else:

                    print()
                    print(
                        "❌ Failed to clear conversation."
                    )

                continue

            # =================================================
            # STATS
            # =================================================

            if question.lower() == "/stats":

                print()
                print("-" * 70)
                print("📊 CONVERSATION STATISTICS")
                print("-" * 70)

                print(
                    f"Conversation ID: "
                    f"{self.rag_service.get_conversation_id()}"
                )

                print(
                    f"Memory Size: "
                    f"{self.rag_service.get_memory_size()}"
                )

                continue

            # =================================================
            # PROCESS QUESTION
            # =================================================

            print()
            print(
                "🧠 NEXUS AI is thinking..."
            )

            try:

                result = (
                    self.rag_service.ask(
                        question
                    )
                )

                self.display_response(
                    result
                )

            except Exception as error:

                print()
                print(
                    "❌ ERROR:"
                )

                print(
                    str(error)
                )