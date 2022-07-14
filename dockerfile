# Version 0.0.1

FROM python:3.9

WORKDIR /app

COPY ./main.py /app/main.py
COPY ./requirements.txt /app/requirements.txt
COPY ./static /app/static

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

CMD ["cd", "/app"]
CMD ["mkdir", "/app/files"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]