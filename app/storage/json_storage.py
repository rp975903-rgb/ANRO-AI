import json
from pathlib import Path


class JSONStorage:
    """
    Simple JSON persistence layer
    for NEXUS AI.
    """


    def __init__(
        self,
        storage_path: str | Path = (
            "data/processed_documents"
        )
    ):

        self.storage_path = Path(
            storage_path
        )


        self.storage_path.mkdir(

            parents=True,

            exist_ok=True

        )


    def save_document(
        self,
        document: dict,
        chunks: list[dict]
    ) -> Path:
        """
        Save document and chunks
        into a JSON file.
        """

        document_id = (
            document["document_id"]
        )


        data = {

            "document":
                document,

            "chunks":
                chunks,

        }


        file_path = (

            self.storage_path

            / f"{document_id}.json"

        )


        with open(

            file_path,

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                data,

                file,

                indent=4,

                ensure_ascii=False

            )


        return file_path


    def load_document(
        self,
        document_id: str
    ) -> dict:

        file_path = (

            self.storage_path

            / f"{document_id}.json"

        )


        if not file_path.exists():

            raise FileNotFoundError(

                f"Stored document not found: "
                f"{document_id}"

            )


        with open(

            file_path,

            "r",

            encoding="utf-8"

        ) as file:

            return json.load(
                file
            )

    def delete_document(
        self,
        document_id: str
    ) -> bool:
        """
        Delete a stored document by ID.
        """

        file_path = (

            self.storage_path

            / f"{document_id}.json"

        )


        if not file_path.exists():

            return False


        file_path.unlink()


        return True