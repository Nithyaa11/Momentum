class NotFoundError(Exception):
    """A requested resource doesn't exist (or belongs to another user)."""

    def __init__(self, resource: str, resource_id: int) -> None:
        super().__init__(f"{resource} {resource_id} not found")
        self.resource = resource
        self.resource_id = resource_id


class ValidationError(Exception):
    """The request is well-formed but refers to something invalid."""
