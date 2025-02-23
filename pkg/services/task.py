from db.models import Task
from pkg.repositories import task as task_repository
from schemas.task import TaskSchema


def get_all_tasks(user_id, is_deleted=False):
    tasks = task_repository.get_all_tasks(user_id, is_deleted)
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


def update_task(user_id: int, task_id: int, task: TaskSchema):
    t = Task()
    t.id = task_id
    t.title = task.title
    t.description = task.description
    t.deadline = "12-12-2025"
    t.priority = task.priority
    t.is_done = False
    t.deleted_at = None
    t.user_id = user_id

    return task_repository.update_task(t)


def delete_task_by_id(user_id, task_id):
    task = task_repository.delete_task_by_id(user_id, task_id)
    return task


def update_task_status_by_id(user_id, task_id, is_done):
    task = task_repository.update_task_status_by_id(user_id, task_id, is_done)
    return task