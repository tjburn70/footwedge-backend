from .abstract_task import AbstractTask
from api_clients.footwedge_search_client import FootwedgeSearchClient
from footwedge_models import User


class SyncUser(AbstractTask):
    def __init__(self, event_name: str, dynamodb_record: dict):
        super(SyncUser, self).__init__(event_name, dynamodb_record)
        self.partition_key = self.keys["pk"]["S"]
        self.user_id = self.partition_key.split("#")[1]

    def build_user(self) -> User:
        birthdate = self.image["birthdate"]["S"]
        gender = self.image["gender"]["S"]
        created_ts = self.image["created_ts"]["S"]
        last_name = self.image["last_name"]["S"]
        phone_number = self.image["phone_number"]["S"]
        first_name = self.image["first_name"]["S"]
        email = self.image["email"]["S"]
        return User(
            user_id=self.user_id,
            email=email,
            first_name=first_name,
            last_name=last_name,
            birthdate=birthdate,
            phone_number=phone_number,
            gender=gender,
            created_ts=created_ts,
        )

    async def process_record(self):
        if self.event_name == "INSERT":
            async with FootwedgeSearchClient() as api_client:
                user = self.build_user()
                return await api_client.add_user(user=user)
