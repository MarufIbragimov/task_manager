import json

from fastapi import APIRouter, status, Depends

from starlette.responses import Response

from pkg.controllers.user import get_current_user, TokenPayload
from pkg.services import task as task_service
from schemas.task import TaskSchema

router = APIRouter()


@router.get("/tasks", summary="Get all tasks", tags=["tasks"])
def get_all_tasks(response: Response, payload: TokenPayload = Depends(get_current_user)):
    user_id = payload.id
    tasks = task_service.get_all_tasks(user_id)
    response.status_code = status.HTTP_200_OK
    response.headers["Content-Type"] = "application/json"
    return tasks


@router.get("/tasks/{task_id}", summary="Get task by ID", tags=["tasks"])
def get_task_by_id(task_id: int, payload: TokenPayload = Depends(get_current_user)):
    user_id = payload.id
    task = task_service.get_task_by_id(user_id, task_id)
    if task is None:
        return Response(json.dumps({'error': 'task not found'}), status.HTTP_404_NOT_FOUND)
    return task


@router.post("/tasks", summary="Create new task", tags=["tasks"])
def create_task(task: TaskSchema, payload: TokenPayload = Depends(get_current_user)):
    user_id = payload.id
    task_service.create_task(user_id, task)

    return Response(json.dumps({'message': 'successfully added new task'}), status_code=201,
                    media_type='application/json')


# "1. Добавить новую задачу" +
# "2. Вывести список задач" +
# "4. Вывести задачу по ID" +
# "3. Редактировать задачу" +
# "5. Удалить задачу по ID" +
# "6. Пометить задачу Выполнено / Не выполнено" +-
# "7. Корзина (вывод удаленных задач)"

@router.put("/tasks/{task_id}", summary="Update task by ID", tags=["tasks"])
def update_task(task_id: int, task: TaskSchema, payload: TokenPayload = Depends(get_current_user)):
    user_id = payload.id
    task_service.update_task(user_id, task_id, task)
   
    return Response(json.dumps({'message': 'successfully updated the task'}), 
                    status.HTTP_200_OK, media_type='application/json')


@router.delete("/tasks/{task_id}", summary="Delete task by ID", tags=["tasks"])
def delete_task(task_id: int, payload: TokenPayload = Depends(get_current_user)):
    user_id = payload.id
    task_service.delete_task_by_id(user_id, task_id)

    return Response(json.dumps({'message': 'successfully deleted the task'})
                    , status.HTTP_200_OK, media_type='application/json')


@router.patch("/tasks/{task_id}/status", summary="Update task status by ID", tags=["tasks"])
def update_task_status_by_id(task_id: int, is_done: bool, payload: TokenPayload = Depends(get_current_user)):
    user_id = payload.id
    task_service.update_task_status_by_id(user_id, task_id, is_done)
    
    return Response(json.dumps({'message': 'successfully updated the task\'s status'}), 
                    status.HTTP_200_OK, media_type='application/json')


@router.get("/tasks/deleted", summary="Get all deleted tasks", tags=["tasks"])
def get_all_deleted_tasks(response: Response, payload: TokenPayload = Depends(get_current_user)):
    user_id = payload.id
    tasks = task_service.get_all_tasks(user_id, is_deleted=True)
    response.status_code = status.HTTP_200_OK
    response.headers["Content-Type"] = "application/json"
    return tasks