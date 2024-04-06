from fastapi import APIRouter

comm = APIRouter()


@comm.get("/")
def one():
    return {"code": 200, "msg": "success", "data": {"name": "one"}}
