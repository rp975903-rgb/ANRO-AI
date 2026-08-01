from app.database.conversation_database import (
    ConversationDatabase
)


def main():

    print()

    print(
        "💾 NEXUS AI CONVERSATION DATABASE TEST"
    )

    print(
        "=" * 60
    )


    # ====================================================
    # CREATE DATABASE
    # ====================================================

    database = ConversationDatabase()


    # ====================================================
    # CONVERSATION ID
    # ====================================================

    conversation_id = (

        "test_conversation_001"

    )


    # ====================================================
    # ADD USER MESSAGE
    # ====================================================

    database.add_message(

        conversation_id=

            conversation_id,

        role="user",

        content="What is Python?"

    )


    # ====================================================
    # ADD ASSISTANT MESSAGE
    # ====================================================

    database.add_message(

        conversation_id=

            conversation_id,

        role="assistant",

        content=(
            "Python is a powerful "
            "programming language."
        )

    )


    # ====================================================
    # GET CONVERSATION
    # ====================================================

    messages = (

        database.get_conversation(

            conversation_id

        )

    )


    print()

    print(
        "📚 STORED CONVERSATION"
    )

    print(
        "-" * 60
    )


    for message in messages:

        print(

            f"{message['role'].upper()}: "

            f"{message['content']}"

        )


    # ====================================================
    # MESSAGE COUNT
    # ====================================================

    count = (

        database.count_messages(

            conversation_id

        )

    )


    print()

    print(

        "🧮 Message Count:",

        count

    )


    # ====================================================
    # RECENT MESSAGES
    # ====================================================

    recent_messages = (

        database.get_recent_messages(

            conversation_id,

            limit=5

        )

    )


    print()

    print(

        "🕐 Recent Messages:",

        len(recent_messages)

    )


    print()

    print(

        "✅ CONVERSATION DATABASE TEST COMPLETED"

    )


if __name__ == "__main__":

    main()