from db.models import Task
from pkg.repositories import task as task_repository
from schemas.task import TaskSchema


def get_all_tasks(user_id):
    tasks = task_repository.get_all_tasks(user_id)
    return tasks


def get_task_by_id(user_id, task_id):
    task = task_repository.get_task_by_id(user_id, task_id)
    return task


def create_task(user_id: int, task: TaskSchema):
    t = Task()
    t.title = task.title
    t.description = task.description
    t.deadline = "12-12-2025"
    t.priority = task.priority
    t.is_done = False
    t.deleted_at = None
    t.user_id = user_id

    return task_repository.create_task(t)
