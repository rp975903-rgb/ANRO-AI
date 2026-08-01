from sentence_transformers import SentenceTransformer


class EmbeddingService:
    """
    Service responsible for converting
    text into numerical vector embeddings.
    """

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2"
    ):

        self.model_name = model_name

        self.model = SentenceTransformer(

            self.model_name

        )


    # ========================================================
    # GENERATE SINGLE EMBEDDING
    # ========================================================

    def generate_embedding(

        self,

        text: str

    ):

        if not text or not text.strip():

            raise ValueError(

                "Text cannot be empty."

            )


        embedding = (

            self.model

            .encode(

                text,

                convert_to_numpy=True

            )

        )


        return embedding


    # ========================================================
    # GENERATE MULTIPLE EMBEDDINGS
    # ========================================================

    def generate_embeddings(

        self,

        texts: list[str]

    ):

        if not texts:

            return []


        embeddings = (

            self.model

            .encode(

                texts,

                convert_to_numpy=True

            )

        )


        return embeddings


    # ========================================================
    # GET EMBEDDING DIMENSION
    # ========================================================

    def get_embedding_dimension(self):

        return (

            self.model

            .get_sentence_embedding_dimension()

        )