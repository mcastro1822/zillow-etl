from pydantic import (
    BaseModel,
    Field,
    RootModel,
)
from pydantic_mongo import AbstractRepository, ObjectIdField


class BaseDocument(BaseModel):
    """
    Base Field for Document
    """

    id: ObjectIdField | None = Field(
        title="Document ID", description="MongoDB ID of the document", default=None
    )


class DocumentSet(RootModel):
    """
    Set Model for collection
    """

    root: list[BaseDocument]

    def __getitem__(self, index: int):
        return self.root[index]

    def __len__(self):
        """
        Length
        """
        return len(self.root)

    def __iter__(self):
        """
        Iter method
        """
        return iter(self.root)


def AbstractRepo(model, model_set, collection: str):
    """
    Creates a abstract repository
    """

    class Repository(AbstractRepository[model]):
        """
        Repository Model
        """

        class Meta:
            collection_name: str = collection

        def get_all(self) -> DocumentSet:
            """
            Grabs all Items in the MongoDB collection
            """
            return model_set(self.find_by({})).root

    return Repository
