from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.predict import router as predict_router

app = FastAPI(title="ApplIQation API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predict_router)
