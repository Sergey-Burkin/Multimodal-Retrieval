import io
import os
import sys

from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from PIL import Image
from sqlalchemy.orm import Session
from src.models import crud
from src.models.database import get_db
from src.schemas import schemas
from src.security import security


ROOT_DIR = "/".join(os.getcwd().split("/")[:-2])
UPLOAD_DIR = "/".join(os.getcwd().split("/")[:-1]) + "/frontend/data"
sys.path.append(ROOT_DIR)
from retrieval.createIndex import CreateModelAndIndex
from retrieval.utils import FindNearestImage


base_router = APIRouter(prefix="", tags=["BaseOps"])


model, preprocess, imageIndex, trainDataset = CreateModelAndIndex(root_dir=ROOT_DIR)


@base_router.get("/")
async def hello_world():
    return {"message": "Hello World"}


@base_router.post("/register", response_model=schemas.User)
async def register(
    username: str,
    password: str,
    db: Session = Depends(get_db),
):
    new_user = schemas.UserCreate(username=username, password=password)
    db_user = crud.get_user_by_username(db, username=new_user.username)

    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user.password = security.get_password_hash(new_user.password)
    return crud.create_user(db=db, user=new_user)


@base_router.post("/login")
async def login(
    username: str,
    password: str,
    db: Session = Depends(get_db),
) -> schemas.Token:
    res = await security.login_for_access_token(
        username=username, password=password, db=db
    )
    return res


@base_router.post("/send_query")
async def send_query(
    file: UploadFile,
    text_query: str = "",
    token: str = "",
    db: Session = Depends(get_db),
):
    try:
        user = await security.get_current_user(token=token, db=db)

        request_object_content = await file.read()
        img = Image.open(io.BytesIO(request_object_content))
        print(img)
        print(type(img))

        nearest_images_names, nearest_pil_images = FindNearestImage(
            img, model, preprocess, imageIndex, trainDataset, upload_dir=UPLOAD_DIR
        )

        for pil_id, pil_image in zip(nearest_images_names, nearest_pil_images):
            print(f"{UPLOAD_DIR}/{pil_id}.jpg")
            pil_image.save(f"{UPLOAD_DIR}/{pil_id}.jpg")

        dict_lst_ans = {"ans": []}
        for name in nearest_images_names:
            dict_lst_ans["ans"].append({"name": f"{name}.jpg", "desc": "Empty"})
        dict_lst_ans["status_code"] = 200
        return dict_lst_ans

    except Exception:
        print(token)
        print("Not Auth")
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        return credentials_exception
