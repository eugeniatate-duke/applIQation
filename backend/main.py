from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routers.predict import router as predict_router

app = FastAPI(title="ApplIQation API")

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"http://localhost:\d+",
    # allow_origins=[
    #     "http://localhost:5173",
    #     "http://localhost:5174",
    #     "https://appliqation.vercel.app",
    # ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predict_router)
