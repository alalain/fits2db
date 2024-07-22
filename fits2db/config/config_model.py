"""
This module contains the configuration validation for the FITS to database application.
"""

from typing import Optional
from typing_extensions import Self

from pydantic import BaseModel, StrictStr, FilePath, model_validator


ACCEPTABLE_TYPES = {"mysql"}


class DatabaseConfig(BaseModel):
    """Database configuration."""

    type: StrictStr
    host: StrictStr
    user: Optional[StrictStr] = None
    password: Optional[StrictStr] = None
    token: Optional[StrictStr] = None
    port: Optional[int] = None

    @model_validator(mode="after")
    def validate_database(self) -> Self:
        """Validate if supported db type"""
        if self.type.lower() not in ACCEPTABLE_TYPES:
            raise ValueError(f"{self.type} is not a supported db")
        return self

    @model_validator(mode="after")
    def check_cedentials(self) -> Self:
        """Validate credentials"""
        user = self.user
        password = self.password
        token = self.token

        if (not user or not password) and not token:
            raise ValueError(
                "Either both user and password must be provided, or token must be provided."
            )

        if token and (user or password):
            raise ValueError(
                "Cannot provide both user/password and token. Use one method for authentication."
            )

        return self


class FitsConfig(BaseModel):
    """Fits files configuraion."""

    name: str


class ConfigFileValidator(BaseModel):
    """Validator if file exists."""

    path: FilePath


class ApplicationConfig(BaseModel):
    """Application configuration."""

    database: DatabaseConfig
    fits_files: FitsConfig


ConfigType = ApplicationConfig