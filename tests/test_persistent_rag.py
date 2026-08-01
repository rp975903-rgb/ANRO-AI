from app.ai.conversation_memory import (
    ConversationMemory
)


def main():

    print()

    print(
        "🧠 NEXUS AI PERSISTENT RAG TEST"
    )

    print(
        "=" * 60
    )


    conversation_id = (

        "nexus_demo_user_001"

    )


    # ====================================================
    # FIRST SESSION
    # ====================================================

    print()

    print(
        "🟢 FIRST SESSION"
    )

    print(
        "-" * 60
    )


    memory = ConversationMemory(

        conversation_id=

            conversation_id,

        max_messages=10

    )


    memory.clear()


    memory.add_user_message(

        "What is Python?"

    )


    memory.add_assistant_message(

        "Python is a programming language."

    )


    print(

        memory.get_messages()

    )


    # ====================================================
    # SIMULATE APPLICATION RESTART
    # ====================================================

    print()

    print(
        "🔄 APPLICATION RESTART"
    )

    print(
        "-" * 60
    )


    del memory


    # ====================================================
    # SECOND SESSION
    # ====================================================

    new_memory = ConversationMemory(

        conversation_id=

            conversation_id,

        max_messages=10

    )


    print()

    print(
        "📥 RESTORED CONVERSATION"
    )

    print(
        "-" * 60
    )


    print(

        new_memory.get_messages()

    )


    # ====================================================
    # VERIFY
    # ====================================================

    if new_memory.size() >= 2:

        print()

        print(
            "✅ PERSISTENT RAG MEMORY WORKING"
        )

    else:

        print()

        print(
            "❌ PERSISTENT MEMORY FAILED"
        )


if __name__ == "__main__":

    main()