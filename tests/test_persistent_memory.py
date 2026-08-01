from app.ai.conversation_memory import (
    ConversationMemory
)


def main():

    print()

    print(
        "🧠 NEXUS AI PERSISTENT MEMORY TEST"
    )

    print(
        "=" * 60
    )


    conversation_id = (

        "persistent_test_001"

    )


    # ====================================================
    # CREATE MEMORY
    # ====================================================

    memory = ConversationMemory(

        conversation_id=

            conversation_id,

        max_messages=10

    )


    # ====================================================
    # CLEAR OLD TEST DATA
    # ====================================================

    memory.clear()


    # ====================================================
    # ADD MESSAGES
    # ====================================================

    memory.add_user_message(

        "What is Python?"

    )


    memory.add_assistant_message(

        "Python is a powerful programming language."

    )


    memory.add_user_message(

        "What is it used for?"

    )


    memory.add_assistant_message(

        "Python is used for web development, AI, automation, and data science."

    )


    # ====================================================
    # DISPLAY MEMORY
    # ====================================================

    print()

    print(
        "📚 CURRENT CONVERSATION"
    )

    print(
        "-" * 60
    )


    print(

        memory.get_messages()

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
    # SIMULATE APPLICATION RESTART
    # ====================================================

    print()

    print(

        "🔄 Simulating application restart..."

    )


    del memory


    # ====================================================
    # CREATE NEW MEMORY INSTANCE
    # ====================================================

    new_memory = ConversationMemory(

        conversation_id=

            conversation_id,

        max_messages=10

    )


    # ====================================================
    # LOAD PERSISTED MEMORY
    # ====================================================

    print()

    print(

        "📥 LOADED AFTER RESTART"

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

    if new_memory.size() == 4:

        print()

        print(

            "✅ PERSISTENT MEMORY TEST PASSED"

        )

    else:

        print()

        print(

            "❌ PERSISTENT MEMORY TEST FAILED"

        )


if __name__ == "__main__":

    main()