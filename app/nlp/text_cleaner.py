import re
import unicodedata


class TextCleaner:
    """
    Professional text cleaning engine
    for the NEXUS AI document pipeline.
    """


    def normalize_unicode(
        self,
        text: str
    ) -> str:
        """
        Normalize Unicode characters.

        This helps keep text representation
        consistent across different documents.
        """

        return unicodedata.normalize(
            "NFKC",
            text
        )


    def remove_control_characters(
        self,
        text: str
    ) -> str:
        """
        Remove unwanted control characters
        while preserving newline and tab.
        """

        cleaned_characters = []


        for character in text:

            category = (
                unicodedata.category(
                    character
                )
            )


            if category.startswith("C"):

                if character in (
                    "\n",
                    "\t",
                ):

                    cleaned_characters.append(
                        character
                    )

                continue


            cleaned_characters.append(
                character
            )


        return "".join(
            cleaned_characters
        )


    def normalize_whitespace(
        self,
        text: str
    ) -> str:
        """
        Normalize spaces and tabs.
        """

        text = re.sub(
            r"[ \t]+",
            " ",
            text
        )


        return text


    def remove_empty_lines(
        self,
        text: str
    ) -> str:
        """
        Remove unnecessary empty lines.
        """

        lines = (
            text.splitlines()
        )


        cleaned_lines = [

            line.strip()

            for line in lines

            if line.strip()

        ]


        return "\n".join(
            cleaned_lines
        )


    def clean(
        self,
        text: str
    ) -> str:
        """
        Run the complete text cleaning pipeline.
        """

        if not isinstance(
            text,
            str
        ):

            raise TypeError(

                "TextCleaner expects "
                "a string input."

            )


        if not text.strip():

            return ""


        # Step 1
        text = (
            self.normalize_unicode(
                text
            )
        )


        # Step 2
        text = (
            self.remove_control_characters(
                text
            )
        )


        # Step 3
        text = (
            self.normalize_whitespace(
                text
            )
        )


        # Step 4
        text = (
            self.remove_empty_lines(
                text
            )
        )


        return text.strip()


    def get_statistics(
        self,
        text: str
    ) -> dict:
        """
        Return basic text statistics.
        """

        words = (
            text.split()
        )


        lines = (
            text.splitlines()
        )


        return {

            "characters":
                len(text),

            "words":
                len(words),

            "lines":
                len(lines),

        }