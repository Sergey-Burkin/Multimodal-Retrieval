FROM python:3.10

RUN pip install poetry==1.4.2

COPY . .

RUN poetry install --without dev

ENTRYPOINT ["poetry", "run", "python3", "retrieval/demo.py"]
