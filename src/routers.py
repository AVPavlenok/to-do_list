from typing import List

from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.responses import Response
from sqlalchemy.exc import IntegrityError

from settings import logger, settings
from src.models import Base, Task, User
from src.database import engine, session, create_item, get_item, patch_item, delete_item
from src.schemas import TaskIn, TaskOut, UserCreate, UserBase
from src.jwt import hash_password, verify_password, create_access_token
from src.auth import get_user_id

app = FastAPI()


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    await session.close()
    await engine.dispose()


@app.post('/register/', status_code=status.HTTP_201_CREATED, summary="Create a new user")
async def register(user: UserCreate):
    user.password = await hash_password(user.password)
    try:
        await create_item(model=User, item=user.dict())
    except IntegrityError:
        raise HTTPException(detail='Such user already exists!', status_code=status.HTTP_409_CONFLICT)
    except Exception:
        raise HTTPException(detail='Try again later!', status_code=status.HTTP_404_NOT_FOUND)
    return "You successfully registered!"


@app.post('/login', status_code=status.HTTP_200_OK, summary='Login for using application')
async def login(user: UserBase, response: Response):
    user_db = await get_item(model=User, login=user.login)
    if not user_db:
        raise HTTPException(detail='No such user. Please register!', status_code=status.HTTP_404_NOT_FOUND)
    is_verify = await verify_password(user.password, user_db[0].password)
    if is_verify:
        access_token = await create_access_token({'id': user_db[0].id, 'login': user_db[0].login})
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            max_age=settings.access_token_expire_seconds
        )
        return "Welcome to our service"
    else:
        raise HTTPException(detail='Access denied', status_code=status.HTTP_401_UNAUTHORIZED)


@app.post('/logout', status_code=status.HTTP_200_OK, summary='Logout from our service')
async def logout(response: Response):
    response.delete_cookie(key="access_token", httponly=True)
    return "You seccessfully logout!"


@app.post('/tasks', status_code=status.HTTP_201_CREATED, summary='Create a new task')
async def create_task(task: TaskIn, user_id: int = Depends(get_user_id)):
    try:
        await create_item(model=Task, item={'task': task.task, 'user_id': user_id})
    except Exception:
        raise HTTPException(detail='Try again later!', status_code=status.HTTP_404_NOT_FOUND)
    return "New task successfully created!"


@app.get('/tasks', response_model=List[TaskOut], status_code=status.HTTP_200_OK, summary='List of all my tasks')
async def get_all_my_tasks(user_id: int = Depends(get_user_id)):
    tasks = await get_item(model=Task, user_id=user_id)
    return tasks


@app.get('/tasks/actual', response_model=List[TaskOut], status_code=status.HTTP_200_OK, summary='List of actual tasks')
async def get_my_actual_tasks(user_id: int = Depends(get_user_id)):
    tasks = await get_item(model=Task, user_id=user_id, is_complete=False)
    return tasks


@app.get('/tasks/{task_id}', response_model=TaskOut, status_code=status.HTTP_200_OK, summary='Get tasks by id')
async def get_task_by_id(task_id: int, user_id: int = Depends(get_user_id)):
    task = await get_item(model=Task, user_id=user_id, id=task_id)
    if not task:
        HTTPException(detail='No such task', status_code=status.HTTP_404_NOT_FOUND)
    return task[0]


@app.patch('/tasks/{task_id}', status_code=status.HTTP_200_OK, summary='Complete the task!')
async def complete_task(task_id: int, user_id: int = Depends(get_user_id)):
    try:
        await patch_item(model=Task, data={'id': task_id, 'user_id': user_id}, new_values={"is_complete": True})
    except Exception:
        raise HTTPException(detail='No such task', status_code=status.HTTP_404_NOT_FOUND)
    return "New task is completed!"


@app.delete('/tasks/{task_id}', status_code=status.HTTP_200_OK, summary='Delete task bu id!')
async def delete_task(task_id: int, user_id: int = Depends(get_user_id)):
    try:
        await delete_item(model=Task, user_id=user_id, id=task_id)
    except Exception:
        raise HTTPException(detail='No such task', status_code=status.HTTP_404_NOT_FOUND)

    return 'Task successfully deleted'
