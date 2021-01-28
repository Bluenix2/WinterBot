from fastapi import Request
from utils import ConnectionUtil


async def get_app(request: Request):
    return request.state.app


async def get_bot(request: Request):
    # In case how we get the app is changed
    return (await get_app(request)).bot


async def get_conn(request: Request):
    return ConnectionUtil((await get_bot(request)).pool)
