from app.config import (
    APP_NAME,
    APP_VERSION,
    APP_ENV,
    create_directories,
)

from app.core.logger import get_logger

from app.core.environment import (
    EnvironmentConfig,
)

from app.database.database_manager import (
    DatabaseManager,
)


class NexusAIApplication:
    """
    Main application controller for NEXUS AI.

    Responsible for:

    - Environment configuration
    - Logging
    - Directory initialization
    - Database initialization
    - Application lifecycle
    """


    def __init__(self):
        """
        Initialize the NEXUS AI application.
        """

        # ====================================================
        # BASIC APPLICATION INFORMATION
        # ====================================================

        self.name = APP_NAME

        self.version = APP_VERSION

        self.environment = APP_ENV


        # ====================================================
        # LOGGER
        # ====================================================

        self.logger = get_logger(
            self.__class__.__name__
        )


        # ====================================================
        # ENVIRONMENT CONFIGURATION
        # ====================================================

        self.environment_config = (
            EnvironmentConfig()
        )


        # ====================================================
        # DATABASE
        # ====================================================

        self.database = (
            DatabaseManager()
        )


        # ====================================================
        # APPLICATION STATE
        # ====================================================

        self.is_initialized = False


    def initialize(self):
        """
        Initialize all core application components.
        """

        self.logger.info(
            "Starting NEXUS AI initialization..."
        )


        # ====================================================
        # CREATE REQUIRED DIRECTORIES
        # ====================================================

        self.logger.info(
            "Creating required directories..."
        )

        create_directories()


        # ====================================================
        # INITIALIZE DATABASE
        # ====================================================

        self.logger.info(
            "Initializing database..."
        )

        self.database.initialize_database()


        # ====================================================
        # MARK APPLICATION AS INITIALIZED
        # ====================================================

        self.is_initialized = True


        self.logger.info(
            "NEXUS AI initialized successfully."
        )


    def get_status(self):
        """
        Return the current application status.
        """

        return {

            "name":
                self.name,

            "version":
                self.version,

            "environment":
                self.environment,

            "initialized":
                self.is_initialized,

            "database":
                str(
                    self.database.database_path
                ),

            "ai_provider":
                self.environment_config.ai_provider,

            "openai_api_key_configured":
                self.environment_config
                .has_openai_api_key(),

        }


    def shutdown(self):
        """
        Shutdown the application safely.
        """

        self.logger.info(
            "Shutting down NEXUS AI..."
        )


        self.is_initialized = False


        self.logger.info(
            "NEXUS AI shutdown complete."
        )