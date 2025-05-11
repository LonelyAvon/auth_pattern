from typing import Optional
from uuid import UUID

from pydantic import BaseModel, model_validator

from app.api.organization.v1.schemas.organization.organization_read import (
    OrganizationRead,
)
from app.api.user.v1.schemas.user.user_read import UserRead


class OrganizationWithUsers(OrganizationRead):
    users: Optional[list[UserRead]]

    @model_validator(mode="after")
    def validate(self):
        if self.users is None:
            self.users = []
        return self
