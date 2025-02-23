import datetime
from sqlalchemy.orm import Session
from db.postgres import engine
from db.models import Task


def get_all_tasks(user_id, is_deleted=False):

    with Session(bind=engine) as db:
        db_tasks = db.query(Task).filter(
            Task.deleted_at != None if is_deleted else Task.deleted_at == None,
            Task.user_id == user_id
        ).all()
        
        tasks = list()
        for task in db_tasks:
            t = Task()
            t.task_id = task.id
            t.title = task.title
            t.description = task.description
            t.deadline = task.deadline
            t.priority = task.priority
            t.is_done = task.is_done
            tasks.append(t)

        return tasks


def get_task_by_id(user_id, task_id):
    with Session(bind=engine) as db:
        db_task = db.query(Task).filter(
            Task.deleted_at == None, 
            Task.user_id == user_id,
            Task.id == task_id
        ).first()
        
        if db_task is None:
            return None

        task = Task()
        task.task_id = db_task.id
        task.title = db_task.title
        task.description = db_task.description
        task.deadline = db_task.deadline
        task.priority = db_task.priority
        task.user_id = db_task.user_id
        task.is_done = db_task.is_done
        return task


def create_task(task: Task):
    with Session(bind=engine) as db:
        task_db = Task(title=task.title,
                       description=task.description,
                       deadline=task.deadline,
                       priority=task.priority,
                       user_id=task.user_id)
        db.add(task_db)
        db.commit()
        return task_db.id


def update_task(task: Task):
    with Session(bind=engine) as db:
        task_to_update = db.query(Task).filter(
            Task.deleted_at == None, 
            Task.user_id == task.user_id,
            Task.id == task.id
        ).first()
        
        if task_to_update is None:
            return None
        
        task_to_update.title = task.title
        task_to_update.description=task.description
        task_to_update.deadline=task.deadline
        task_to_update.priority=task.priority
        task_to_update.user_id=task.user_id
        db.commit()
        
        return task_to_update.id
        

def delete_task_by_id(user_id, task_id):
    with Session(bind=engine) as db:
        task_to_be_deleted = db.query(Task).filter(
            Task.deleted_at == None, 
            Task.user_id == user_id,
            Task.id == task_id
        ).first()
        
        if task_to_be_deleted is None:
            return None
        
        task_to_be_deleted.deleted_at = datetime.datetime.now()
        db.commit()

        return task_to_be_deleted.id
    

def update_task_status_by_id(user_id, task_id, is_done):
    with Session(bind=engine) as db:
        task_to_be_ticked = db.query(Task).filter(
            Task.deleted_at == None, 
            Task.user_id == user_id,
            Task.id == task_id
        ).first()
        
        if task_to_be_ticked is None:
            return None
        
        task_to_be_ticked.is_done = is_done
        db.commit()

        return task_to_be_ticked.id

