import os

from app.core.settings import BaseAppSettings, Settings


def get_settings() -> BaseAppSettings:
    """
    Retrieve the application settings based on the current environment.

    This function reads the 'ENVIRONMENT' environment variable
    and returns a settings instance.

    Returns:
        BaseAppSettings:
        The settings instance for the current environment.
    """

    environment = os.environ.get("ENVIRONMENT", "local")

    if environment == "docker":
        return Settings()
    return BaseAppSettings()
