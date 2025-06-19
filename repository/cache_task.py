import json

from redis import Redis

from schemas.task import TaskSchema


class TaskCache:
    def __init__(self, redis: Redis):
        self.redis = redis

    def get_tasks(self) -> list[TaskSchema]:
        with self.redis as redis:
            redis.expire('tasks', 25)
            tasks_json = redis.lrange('tasks', 0, -1)
            return [TaskSchema.model_validate(json.loads(task)) for task in tasks_json]

    def set_tasks(self, tasks: list[TaskSchema]):
        tasks_json = [task.model_dump_json() for task in tasks]
        if tasks:
            with self.redis as redis:
                redis.lpush('tasks', *tasks_json)

    def drop_tasks(self):
        with self.redis as redis:
            redis.delete('tasks')
