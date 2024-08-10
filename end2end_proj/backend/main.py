from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from src.models import models
from src.models.database import engine
from src.routs.routs import base_router


# from src.retrieval.createIndex import CreateModelAndIndex
# from src.retrieval.utils import FindNearestImage
# from src.retrieval.demo import PrintHi


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


origins = ["http://localhost:8000", "http://localhost:3000", "https://localhost:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

app.include_router(base_router)
