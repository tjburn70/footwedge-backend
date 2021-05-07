from typing import Dict

from pydantic import BaseModel


class User(BaseModel):
    user_info: Dict

    @property
    def email(self):
        return self.user_info["cognito:email"]

    @property
    def username(self):
        return self.user_info["cognito:username"]
