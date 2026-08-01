from abc import ABC, abstractmethod


class BaseLLM(ABC):
    """
    Abstract base class for all LLM providers.

    Every LLM implementation must provide
    a generate() method.
    """

    @abstractmethod
    def generate(
        self,
        prompt: str
    ) -> str:
        """
        Generate a response from the LLM.
        """

        raise NotImplementedError(
            "LLM implementations must implement "
            "the generate() method."
        )