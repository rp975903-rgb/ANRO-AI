from app.database.conversation_database import (
    ConversationDatabase
)


class ConversationMemory:
    """
    Persistent conversation memory.

    Stores conversation messages in SQLite
    so memory survives application restarts.
    """

    def __init__(
        self,
        conversation_id: str = "default_conversation",
        max_messages: int = 10
    ):

        if not conversation_id.strip():

            raise ValueError(
                "Conversation ID cannot be empty."
            )


        if max_messages <= 0:

            raise ValueError(
                "max_messages must be greater than zero."
            )


        self.conversation_id = (
            conversation_id
        )

        self.max_messages = (
            max_messages
        )


        # ====================================================
        # DATABASE
        # ====================================================

        self.database = (

            ConversationDatabase()

        )


    # ========================================================
    # ADD USER MESSAGE
    # ========================================================

    def add_user_message(
        self,
        message: str
    ):

        if not isinstance(
            message,
            str
        ):

            raise TypeError(
                "Message must be a string."
            )


        message = message.strip()


        if not message:

            raise ValueError(
                "Message cannot be empty."
            )


        self.database.add_message(

            conversation_id=
                self.conversation_id,

            role="user",

            content=message

        )


    # ========================================================
    # ADD ASSISTANT MESSAGE
    # ========================================================

    def add_assistant_message(
        self,
        message: str
    ):

        if not isinstance(
            message,
            str
        ):

            raise TypeError(
                "Message must be a string."
            )


        message = message.strip()


        if not message:

            raise ValueError(
                "Message cannot be empty."
            )


        self.database.add_message(

            conversation_id=
                self.conversation_id,

            role="assistant",

            content=message

        )


    # ========================================================
    # GET MESSAGES
    # ========================================================

    def get_messages(self):

        messages = (

            self.database

            .get_recent_messages(

                conversation_id=
                    self.conversation_id,

                limit=
                    self.max_messages

            )

        )


        formatted_messages = []


        for message in messages:

            role = (

                message.get(

                    "role",

                    "unknown"

                )

            )


            content = (

                message.get(

                    "content",

                    ""

                )

            )


            formatted_messages.append(

                f"{role.upper()}: {content}"

            )


        return "\n".join(

            formatted_messages

        )


    # ========================================================
    # GET RAW MESSAGES
    # ========================================================

    def get_raw_messages(self):

        return (

            self.database

            .get_recent_messages(

                conversation_id=
                    self.conversation_id,

                limit=
                    self.max_messages

            )

        )


    # ========================================================
    # GET MEMORY SIZE
    # ========================================================

    def size(self):

        return (

            self.database

            .count_messages(

                self.conversation_id

            )

        )


    # ========================================================
    # CLEAR MEMORY
    # ========================================================

    def clear(self):

        return (

            self.database

            .delete_conversation(

                self.conversation_id

            )

        )


    # ========================================================
    # GET CONVERSATION ID
    # ========================================================

    def get_conversation_id(self):

        return (

            self.conversation_id

        )