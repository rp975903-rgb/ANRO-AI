class RetrievalAnalyzer:
    """
    Analyzes retrieval results and calculates
    a more reliable confidence score for the RAG pipeline.
    """

    def __init__(
        self,
        strong_threshold: float = 0.35,
        medium_threshold: float = 0.70
    ):
        """
        Initialize retrieval analyzer.
        """

        self.strong_threshold = (
            strong_threshold
        )

        self.medium_threshold = (
            medium_threshold
        )


    # ========================================================
    # ANALYZE RESULTS
    # ========================================================

    def analyze(
        self,
        retrieval_results: list[dict]
    ) -> dict:
        """
        Analyze retrieved document chunks
        and calculate retrieval confidence.
        """

        # ====================================================
        # NO RESULTS
        # ====================================================

        if not retrieval_results:

            return {

                "confidence_score": 0.0,

                "confidence_level": "low",

                "result_count": 0,

                "average_distance": None,

                "best_distance": None,

                "retrieval_quality": "no_results",

            }


        # ====================================================
        # EXTRACT VALID DISTANCES
        # ====================================================

        distances = [

            result.get(
                "distance"
            )

            for result in retrieval_results

            if result.get(
                "distance"
            ) is not None

        ]


        # ====================================================
        # NO VALID DISTANCES
        # ====================================================

        if not distances:

            return {

                "confidence_score": 0.0,

                "confidence_level": "unknown",

                "result_count":
                    len(
                        retrieval_results
                    ),

                "average_distance": None,

                "best_distance": None,

                "retrieval_quality":
                    "distance_unavailable",

            }


        # ====================================================
        # CALCULATE DISTANCES
        # ====================================================

        best_distance = min(
            distances
        )


        average_distance = (

            sum(
                distances
            )

            / len(
                distances
            )

        )


        # ====================================================
        # CALCULATE BASE CONFIDENCE
        # ====================================================

        confidence_score = (

            1.0

            - best_distance

        )


        # Keep score between 0 and 1

        confidence_score = max(

            0.0,

            min(

                1.0,

                confidence_score

            )

        )


        # ====================================================
        # DETERMINE CONFIDENCE LEVEL
        # ====================================================

        if (

            best_distance

            <= self.strong_threshold

        ):

            confidence_level = (

                "high"

            )


        elif (

            best_distance

            <= self.medium_threshold

        ):

            confidence_level = (

                "medium"

            )


        else:

            confidence_level = (

                "low"

            )


        # ====================================================
        # DETERMINE RETRIEVAL QUALITY
        # ====================================================

        if best_distance <= 0.35:

            retrieval_quality = (

                "strong_match"

            )


        elif best_distance <= 0.70:

            retrieval_quality = (

                "moderate_match"

            )


        elif best_distance <= 1.0:

            retrieval_quality = (

                "weak_match"

            )


        else:

            retrieval_quality = (

                "very_weak_match"

            )


        # ====================================================
        # RETURN ANALYSIS
        # ====================================================

        return {

            "confidence_score":

                round(

                    confidence_score,

                    3

                ),

            "confidence_level":

                confidence_level,

            "result_count":

                len(

                    retrieval_results

                ),

            "average_distance":

                round(

                    average_distance,

                    3

                ),

            "best_distance":

                round(

                    best_distance,

                    3

                ),

            "retrieval_quality":

                retrieval_quality,

        }