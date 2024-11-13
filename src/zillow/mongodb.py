from prefect.blocks.core import Block
from pydantic.version import VERSION as PYDANTIC_VERSION
from pymongo import MongoClient

HAS_PYDANTIC_V2 = PYDANTIC_VERSION.startswith("2.")

if HAS_PYDANTIC_V2:
    from pydantic.v1 import SecretStr, root_validator
else:
    from pydantic import SecretStr, root_validator


class MongoDB(Block):
    """
    MongoDB access block
    """

    host: str
    username: str | None = None
    password: SecretStr | None = None

    _block_type_name = "MongoDB"

    @root_validator
    def validate_input(cls, values):
        """
        Verifies that a username and password are provided
        """
        if values["username"] is None and values["password"] is None:
            raise ValueError("Username and password must be specifed")
        else:
            return values

    def get_client(self) -> MongoClient:
        return MongoClient(
            host=self.host,
            username=self.username,
            password=self.password.get_secret_value(),
        )
