from abc import (
    ABCMeta,
    abstractmethod,
)


class AbstractTask(metaclass=ABCMeta):

    def __init__(self, event_name: str, dynamodb_record: dict):
        self.event_name = event_name
        self.keys = dynamodb_record['Keys']
        self.image = dynamodb_record.get('NewImage')

    @abstractmethod
    async def process_record(self):
        raise NotImplementedError
