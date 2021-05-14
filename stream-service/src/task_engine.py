import asyncio

from tasks.abstract_task import AbstractTask


class TaskEngine:

    def __init__(self, *tasks: AbstractTask):
        self._tasks = tasks

    async def execute_tasks(self):
        input_coroutines = [task.process_record() for task in self._tasks]
        return await asyncio.gather(*input_coroutines)

    def run(self):
        event_loop = asyncio.get_event_loop()
        return event_loop.run_until_complete(self.execute_tasks())
