from fastapi import Cookie, HTTPException, Depends, Header
from starlette import status
from starlette.requests import Request

from demo.config import session_storage
from demo.models import User
from demo.utils import verify_jwt
from src.dependencies import DBSession


async def _check_session(
    session: DBSession, request: Request, authorization: str = Header()
):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    payload = verify_jwt(jwt=authorization.removeprefix("Bearer "))

    user = await session.get(entity=User, ident=payload.get("sub"))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    request.session.update(user=user.id)


# async def _authenticate(request: Request):
#     authorization = request.headers.get("cookie")
#     if authorization is None:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
#
#     if not authorization.startswith("access_token=Bearer "):
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
#
#     token = authorization.removeprefix("access_token=Bearer ")
#     try:
#         payload = verify_jwt(jwt=token)
#     except ValueError as e:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'{e}')
#     request.state.user = payload


async def _authenticate(session: DBSession, request: Request):
    # authorization = request.cookies.get("access_token")   # -> "Bearer xxx" или None
    # if not authorization or not authorization.startswith("Bearer "):
    #     raise HTTPException(status_code=403)
    # token = authorization.removeprefix("Bearer ")
    authorization = request.headers.get("cookie")
    if authorization is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    if not authorization.startswith("access_token=Bearer "):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    token = authorization.removeprefix("access_token=Bearer ")
    try:
        payload = verify_jwt(jwt=token)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'{e}')
    user = await session.get(entity=User, ident=payload.get("sub"))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    user_name = user.email
    # print(user_name)
    # request.session.update(user=user.id)
    request.state.user = payload
    # print(request.state.user)
    return user_name

async def _check_user(session: DBSession, request: Request):
    authorization = request.headers.get("cookie")
    if authorization is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    if not authorization.startswith("access_token=Bearer "):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    token = authorization.removeprefix("access_token=Bearer ")
    try:
        payload = verify_jwt(jwt=token)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'{e}')
    user = await session.get(entity=User, ident=payload.get("sub"))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    user = user.email
    # print(user_name)
    # request.session.update(user=user.id)
    request.state.user = payload
    # print(request.state.user)
    return user


authenticate = Depends(dependency=_authenticate)
check_session = Depends(dependency=_check_session)
