from .abstract_task import AbstractTask


class SyncGolfClub(AbstractTask):

    async def process_record(self):
        print(f"hello i'm {self.__class__} processing a record: {self.image}")
