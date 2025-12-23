from src.models import Task, User
from src.jwt import hash_password

user_demo = [
    {
        'name': 'name1',
        'login': 'login1',
        'password': 'password1',
    },
    {
        'name': 'name2',
        'login': 'login2',
        'password': 'password2',
    },
    {
        'name': 'name3',
        'login': 'login3',
        'password': 'password3',
    },
]

task_demo = [
    {
        'user_id': 1,
        'task': 'New task #1 by user #1'
    },
    {
        'user_id': 1,
        'task': 'New task #2 by user #1'
    },
    {
        'user_id': 1,
        'task': 'New task #3 by user #1'
    },
    {
        'user_id': 2,
        'task': 'New task #1 by user #2'
    },
    {
        'user_id': 2,
        'task': 'New task #2 by user #2'
    },
    {
        'user_id': 2,
        'task': 'New task #3 by user #2'
    },
    {
        'user_id': 3,
        'task': 'New task #1 by user #3'
    },
    {
        'user_id': 3,
        'task': 'New task #2 by user #3'
    },
    {
        'user_id': 3,
        'task': 'New task #3 by user #3'
    },
]


async def load_demo_db(session):
    async with session.begin():
        session.add_all(
            [User(**item) for item in user_demo]
        )

    async with session.begin():
        session.add_all(
            [Task(**item) for item in task_demo]
        )

