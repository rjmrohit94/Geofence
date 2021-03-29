FROM python:3.8.1-slim AS compile-image

RUN apt-get update && apt-get install -y --no-install-recommends build-essential gcc make

WORKDIR /app

RUN python -m venv /home/venv
ENV PATH="/home/venv/bin:$PATH"

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt


FROM python:3.8.1-slim AS build-image

WORKDIR /app
COPY --from=compile-image /home/venv /home/venv
ENV PATH="/home/venv/bin:$PATH"

COPY . /app

EXPOSE 5001
CMD ["python", "run.py"]
