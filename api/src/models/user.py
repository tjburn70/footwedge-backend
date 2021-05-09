from typing import Dict

from pydantic import BaseModel


class CognitoUser(BaseModel):
    user_info: Dict

    @property
    def email(self):
        return self.user_info["email"]

    @property
    def username(self):
        return self.user_info["sub"]
