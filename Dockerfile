FROM python:3.11-slim

WORKDIR /app

RUN pip install uv

COPY requirements*.txt ./
ARG ENV=prod
RUN if [ "$ENV" = "dev" ] ; then uv pip install -r requirements-dev.txt --system ; else uv pip install -r requirements.txt --system ; fi

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]