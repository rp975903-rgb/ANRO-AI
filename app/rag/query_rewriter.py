class QueryRewriter:
    """
    Rewrites follow-up questions into
    standalone search queries.

    Example:

    Conversation:
        User: What is Python?
        Assistant: Python is a programming language.

    Follow-up:
        What is it used for?

    Rewritten Query:
        What is Python used for?
    """

    def __init__(
        self,
        max_history_messages: int = 6
    ):

        if max_history_messages <= 0:

            raise ValueError(
                "max_history_messages "
                "must be greater than zero."
            )


        self.max_history_messages = (
            max_history_messages
        )


    # ========================================================
    # REWRITE QUERY
    # ========================================================

    def rewrite(
        self,
        question: str,
        conversation_history: list[dict] | None = None
    ) -> str:
        """
        Convert a follow-up question into
        a standalone search query.
        """

        if not isinstance(
            question,
            str
        ):

            raise TypeError(
                "Question must be a string."
            )


        question = question.strip()


        if not question:

            raise ValueError(
                "Question cannot be empty."
            )


        if not conversation_history:

            return question


        recent_history = (

            conversation_history[
                -self.max_history_messages:
            ]

        )


        # ====================================================
        # GET PREVIOUS USER QUESTIONS
        # ====================================================

        previous_questions = [

            message.get(
                "content",
                ""
            )

            for message in recent_history

            if message.get(
                "role"
            ) == "user"

        ]


        if not previous_questions:

            return question


        last_question = (

            previous_questions[-1]

        )


        # ====================================================
        # SIMPLE REFERENCE RESOLUTION
        # ====================================================

        rewritten_question = (

            question

        )


        replacements = {

            "it":
                last_question,

            "this":
                last_question,

            "that":
                last_question,

        }


        question_lower = (

            question.lower()

        )


        for reference, previous in (

            replacements.items()

        ):

            if (

                question_lower.startswith(

                    f"{reference} "

                )

                or question_lower.startswith(

                    f"{reference}?"

                )

            ):

                rewritten_question = (

                    f"Regarding "

                    f"'{previous}', "

                    f"{question}"

                )

                break


        return rewritten_question