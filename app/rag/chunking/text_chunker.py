from dataclasses import dataclass, field
from typing import List
from uuid import uuid4


@dataclass
class TextChunk:

    text: str

    chunk_index: int

    document_id: str

    chunk_id: str = field(
        default_factory=lambda: str(uuid4())
    )

    start_position: int = 0

    end_position: int = 0

    metadata: dict = field(
        default_factory=dict
    )


    def to_dict(self) -> dict:

        return {

            "chunk_id":
                self.chunk_id,

            "document_id":
                self.document_id,

            "chunk_index":
                self.chunk_index,

            "text":
                self.text,

            "start_position":
                self.start_position,

            "end_position":
                self.end_position,

            "metadata":
                self.metadata,

        }


class TextChunker:

    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 50
    ):

        if chunk_size <= 0:

            raise ValueError(
                "Chunk size must be greater than zero."
            )


        if chunk_overlap < 0:

            raise ValueError(
                "Chunk overlap cannot be negative."
            )


        if chunk_overlap >= chunk_size:

            raise ValueError(
                "Chunk overlap must be smaller "
                "than chunk size."
            )


        self.chunk_size = chunk_size

        self.chunk_overlap = chunk_overlap


    def create_chunks(
        self,
        text: str,
        document_id: str
    ) -> List[TextChunk]:

        if not text.strip():

            return []


        chunks = []

        start = 0

        chunk_index = 0

        text_length = len(text)


        while start < text_length:

            end = min(

                start + self.chunk_size,

                text_length

            )


            chunk_text = (

                text[start:end]

                .strip()

            )


            if chunk_text:

                chunk = TextChunk(

                    text=chunk_text,

                    chunk_index=chunk_index,

                    document_id=document_id,

                    start_position=start,

                    end_position=end,

                    metadata={

                        "chunk_size":
                            len(chunk_text),

                        "document_id":
                            document_id,

                    }

                )


                chunks.append(
                    chunk
                )


                chunk_index += 1


            next_start = (

                end

                - self.chunk_overlap

            )


            if next_start <= start:

                break


            start = next_start


        return chunks