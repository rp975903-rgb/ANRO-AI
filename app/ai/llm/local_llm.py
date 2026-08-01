
from app.ai.llm.base_llm import BaseLLM
import ollama


class LocalLLM(BaseLLM):

    def __init__(
        self,
        model_name: str = "llama3.2:3b"
    ):

        if not isinstance(
            model_name,
            str
        ):
            raise TypeError(
                "Model name must be a string."
            )

        model_name = model_name.strip()

        if not model_name:
            raise ValueError(
                "Model name cannot be empty."
            )

        self.model_name = model_name


    def generate(
        self,
        prompt: str
    ) -> str:

        if not isinstance(
            prompt,
            str
        ):
            raise TypeError(
                "Prompt must be a string."
            )

        prompt = prompt.strip()

        if not prompt:
            raise ValueError(
                "Prompt cannot be empty."
            )


        try:

            response = ollama.chat(

                model=self.model_name,

                messages=[

                    {
                        "role": "user",
                        "content": prompt
                    }

                ]

            )
            print("\n" + "=" * 60)
            print("OLLAMA RESPONSE DEBUG")
            print("=" * 60)

            print("RAW RESPONSE:")
            print(response)

            print("RESPONSE TYPE:")
            print(type(response))

            print("MESSAGE:")
            print(response.message)

            print("MESSAGE TYPE:")
            print(type(response.message))

            print("CONTENT:")
            print(response.message.content)

            print("=" * 60)

        except Exception as error:

            raise RuntimeError(

                "Failed to generate response "
                "from Ollama local LLM. "

                f"Model: {self.model_name}. "

                f"Error: {error}"

            ) from error


        if response is None:

            raise RuntimeError(
                "Ollama returned None response."
            )


        # Ollama Python Client 0.6.2
        # returns ChatResponse object

        message = response.message


        if message is None:

            raise RuntimeError(
                "Ollama returned an empty message."
            )


        answer = message.content


        if answer is None:

            raise RuntimeError(
                "Ollama returned None content."
            )


        answer = str(
            answer
        ).strip()


        if not answer:

            raise RuntimeError(
                "Ollama returned empty content."
            )


        return answer
    
