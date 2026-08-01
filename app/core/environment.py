import os

from dotenv import load_dotenv


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


class EnvironmentConfig:
    """
    Central manager for environment configuration.
    """

    def __init__(self):

        self.app_env = os.getenv(
            "APP_ENV",
            "development"
        )

        self.ai_provider = os.getenv(
            "AI_PROVIDER",
            "local"
        )

        self.openai_api_key = os.getenv(
            "OPENAI_API_KEY"
        )

        self.local_model_name = os.getenv(
            "LOCAL_MODEL_NAME"
        )

        self.database_url = os.getenv(
            "DATABASE_URL",
            "sqlite:///data/database/nexus_ai.db"
        )

        self.log_level = os.getenv(
            "LOG_LEVEL",
            "INFO"
        )


    def is_production(self) -> bool:
        """
        Check whether application is running
        in production environment.
        """

        return (
            self.app_env.lower()
            == "production"
        )


    def has_openai_api_key(self) -> bool:
        """
        Check whether OpenAI API key exists.
        """

        return bool(
            self.openai_api_key
        )


    def get_summary(self) -> dict:
        """
        Return safe configuration summary.

        Sensitive values are not exposed.
        """

        return {

            "app_env":
                self.app_env,

            "ai_provider":
                self.ai_provider,

            "openai_api_key_configured":
                self.has_openai_api_key(),

            "local_model_name":
                self.local_model_name,

            "database_url":
                self.database_url,

            "log_level":
                self.log_level,

        }