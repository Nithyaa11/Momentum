from typing import ClassVar, Self

from pydantic import BaseModel, model_validator


class PartialUpdate(BaseModel):
    """Base for PATCH bodies: fields may be omitted, but fields listed in
    `non_nullable` can't be explicitly set to null."""

    non_nullable: ClassVar[tuple[str, ...]] = ()

    @model_validator(mode="after")
    def _reject_nulls(self) -> Self:
        for field in self.non_nullable:
            if field in self.model_fields_set and getattr(self, field) is None:
                raise ValueError(f"{field} cannot be null")
        return self
