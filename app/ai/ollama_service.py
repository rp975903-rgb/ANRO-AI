from typing import Any

import requests


class OllamaService:
    """
    Service responsible for communicating
    with the local Ollama LLM server.

    ANRO AI uses Ollama to generate answers
    from RAG prompts.
    """

    def __init__(
        self,
        base_url: str = "http://localhost:11434",
        model_name: str = "llama3.2:3b",
        timeout: int = 120,
    ):
        """
        Initialize Ollama service.
        """

        self.base_url = (
            base_url.rstrip("/")
        )

        self.model_name = (
            model_name
        )

        self.timeout = (
            timeout
        )

        self.generate_url = (
            f"{self.base_url}/api/generate"
        )


    # ========================================================
    # CHECK OLLAMA SERVER
    # ========================================================

    def is_available(
        self,
    ) -> bool:
        """
        Check whether Ollama server
        is available.
        """

        try:

            response = requests.get(

                self.base_url,

                timeout=10,

            )

            return (
                response.status_code
                == 200
            )

        except requests.RequestException:

            return False


    # ========================================================
    # CHECK MODEL
    # ========================================================

    def is_model_available(
        self,
    ) -> bool:
        """
        Check whether configured model
        is available in Ollama.
        """

        try:

            response = requests.get(

                f"{self.base_url}/api/tags",

                timeout=10,

            )

            response.raise_for_status()

            data = (
                response.json()
            )

            models = data.get(

                "models",

                []

            )

            for model in models:

                model_name = (
                    model.get(
                        "name",
                        ""
                    )
                )

                if model_name == (
                    self.model_name
                ):

                    return True

            return False

        except requests.RequestException:

            return False


    # ========================================================
    # GENERATE RESPONSE
    # ========================================================

    def generate(
        self,
        prompt: str,
    ) -> str:
        """
        Generate an AI response
        using Ollama.
        """

        if not prompt:

            raise ValueError(

                "Prompt cannot be empty."

            )


        prompt = (
            prompt.strip()
        )


        # ====================================================
        # CHECK OLLAMA SERVER
        # ====================================================

        if not self.is_available():

            raise ConnectionError(

                "Ollama server is not available. "
                "Please make sure Ollama is running."

            )


        # ====================================================
        # GENERATE REQUEST
        # ====================================================

        payload = {

            "model":
                self.model_name,

            "prompt":
                prompt,

            "stream":
                False,

        }


        try:

            response = requests.post(

                self.generate_url,

                json=payload,

                timeout=self.timeout,

            )

            response.raise_for_status()


            data = (
                response.json()
            )


            answer = (
                data.get(
                    "response",
                    ""
                )
            )


            if not answer:

                raise ValueError(

                    "Ollama returned an empty response."

                )


            return (
                answer.strip()
            )


        except requests.RequestException as error:

            raise RuntimeError(

                f"Ollama request failed: "
                f"{error}"

            ) from error


    # ========================================================
    # GENERATE RAG RESPONSE
    # ========================================================

    def generate_rag_response(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> str:
        """
        Generate an answer using
        separate system and user prompts.
        """

        if not system_prompt:

            raise ValueError(

                "System prompt cannot be empty."

            )


        if not user_prompt:

            raise ValueError(

                "User prompt cannot be empty."

            )


        combined_prompt = (

            f"System Instructions:\n\n"

            f"{system_prompt}\n\n"

            f"User Request:\n\n"

            f"{user_prompt}"

        )


        return self.generate(

            combined_prompt

        )


    # ========================================================
    # GENERATE FROM RAG MESSAGES
    # ========================================================

    def generate_from_messages(
        self,
        messages: list[dict[str, str]],
    ) -> str:
        """
        Generate an answer from
        system/user chat messages.
        """

        if not messages:

            raise ValueError(

                "Messages cannot be empty."

            )


        prompt_parts = []


        for message in messages:

            role = (

                message.get(

                    "role",

                    "user"

                )

            )


            content = (

                message.get(

                    "content",

                    ""

                )

            ).strip()


            if not content:

                continue


            prompt_parts.append(

                f"{role.upper()}:\n"
                f"{content}"

            )


        if not prompt_parts:

            raise ValueError(

                "No valid message content found."

            )


        combined_prompt = (

            "\n\n".join(

                prompt_parts

            )

        )


        return self.generate(

            combined_prompt

        )


    # ========================================================
    # GET SERVICE STATUS
    # ========================================================

    def get_status(
        self,
    ) -> dict[str, Any]:
        """
        Return Ollama service status.
        """

        server_available = (
            self.is_available()
        )

        model_available = False


        if server_available:

            model_available = (

                self.is_model_available()

            )


        return {

            "service":
                "Ollama",

            "base_url":
                self.base_url,

            "model":
                self.model_name,

            "server_available":
                server_available,

            "model_available":
                model_available,

            "ready":
                (
                    server_available
                    and model_available
                ),

        }