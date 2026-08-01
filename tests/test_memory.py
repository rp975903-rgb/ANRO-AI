from app.ai.conversation_memory import (
    ConversationMemory
)


def main():

    print()

    print(
        "🧠 NEXUS AI CONVERSATION MEMORY TEST"
    )

    print(
        "=" * 60
    )


    # ====================================================
    # CREATE MEMORY
    # ====================================================

    memory = ConversationMemory(

        max_messages=10

    )


    # ====================================================
    # ADD USER MESSAGE
    # ====================================================

    memory.add_user_message(

        "What is Python?"

    )


    # ====================================================
    # ADD ASSISTANT MESSAGE
    # ====================================================

    memory.add_assistant_message(

        "Python is a powerful programming language."

    )


    # ====================================================
    # ADD SECOND USER MESSAGE
    # ====================================================

    memory.add_user_message(

        "What is it used for?"

    )


    # ====================================================
    # DISPLAY MEMORY
    # ====================================================

    print()

    print(
        "📚 CONVERSATION HISTORY"
    )

    print(
        "-" * 60
    )


    print(

        memory.get_history_text()

    )


    # ====================================================
    # MEMORY SIZE
    # ====================================================

    print()

    print(

        "🧮 Memory Size:",

        memory.size()

    )


    # ====================================================
    # RECENT MESSAGES
    # ====================================================

    print()

    print(

        "🕐 RECENT MESSAGES"

    )

    print(

        "-" * 60

    )


    for message in (

        memory.get_recent_messages(

            3

        )

    ):

        print(

            f"{message['role']}: "
            f"{message['content']}"

        )


    print()

    print(
        "✅ MEMORY TEST COMPLETED"
    )


if __name__ == "__main__":

    main()