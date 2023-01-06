from fastapi import FastAPI
import akshare as ak
from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from app.schemas import UserOut, UserAuth, TokenSchema
from replit import db
from app.utils import (
    get_hashed_password,
    create_access_token,
    create_refresh_token,
    verify_password
)
from uuid import uuid4

from fastapi.middleware.cors import CORSMiddleware


# uvicorn main:app --reload --port 9000


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:9000",
    # 客户端的源
    "http://localhost:3000"
]

# C、配置 CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 允许访问的源
    allow_credentials=True,  # 支持 cookie
    allow_methods=["*"],  # 允许使用的请求方法
    allow_headers=["*"]  # 允许携带的 Headers
)


@app.get("/hello")
async def root():
    stock_sse_summary_df = ak.stock_sse_summary()

    # gegu
    stock_individual_info_em_df = ak.stock_individual_info_em(symbol="601985")




    return stock_sse_summary_df


@app.post('/login', summary="Create access and refresh tokens for user", response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.get(form_data.username, None)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    hashed_pass = user['password']
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    return {
        "access_token": create_access_token(user['email']),
        "refresh_token": create_refresh_token(user['email']),
    }







# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return "5173"
