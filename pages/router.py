from fastapi import APIRouter, Request, Depends, Form
from sqlalchemy import select

from demo.dependencies import check_session, authenticate, _authenticate
from demo.handlers.v1.cases import cases_list, case_detail, case_detail_user
from demo.handlers.v1.comments import comment_detail
from demo.models import User
from demo.schemas import CaseDetail
from src.config import templating
from src.dependencies import DBSession
from jwt import encode, decode
from demo.config import pwd_context, config

# from demo.__main__ import signin
router = APIRouter(
    prefix="/cases",
    tags=["Pages"]
    #dependencies=[authenticate]
)


@router.get("/")
def get_base_page(request: Request, user=Depends(_authenticate)):
    return templating.TemplateResponse("demo/index.html", {"request": request, "user": user})


@router.get("/list")
def get_list_page(request: Request, cases=Depends(cases_list), user=Depends(_authenticate)):
    return templating.TemplateResponse("demo/case_list.html", {"request": request, "cases": cases, "user": user})


@router.get("/list/{pk}")
def get_list_page(request: Request, comments=Depends(comment_detail), cases=Depends(case_detail), user=Depends(_authenticate)):
    return templating.TemplateResponse("demo/case_detail.html", {"request": request, "comments": comments, "cases": cases, "user": user})


@router.get('/create')
def get_create_form(request: Request, user=Depends(_authenticate)):
    return templating.TemplateResponse('demo/form.html', {'request': request, "user": user})


@router.get('/profile')
def get_profile(request: Request, user=Depends(_authenticate), cases=Depends(case_detail_user)):
    return templating.TemplateResponse('demo/profile.html', {'request': request, "cases": cases, "user": user})

