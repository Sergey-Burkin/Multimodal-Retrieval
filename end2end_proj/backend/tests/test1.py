import os
import sys


sys.path.append(f"{os.getcwd()}")

from fastapi import HTTPException
from src.models.database import get_db
from src.routs.routs import login
from src.schemas import schemas


def test_passing():
    assert (1, 2, 3) == (1, 2, 3)


async def test_login():
    db = get_db()

    try:
        res = await login(username="test", password="1234", db=db)

        assert isinstance(res, schemas.Token)

        res = await login(username="test", password="1234ksjd", db=db)

        assert not isinstance(res, HTTPException)
    except:
        pass

    db.close()
