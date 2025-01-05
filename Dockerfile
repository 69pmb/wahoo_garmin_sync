FROM python:3.10-alpine3.21

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1
# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --upgrade pip && pip install --no-cache-dir garth flask

COPY server.py /app/server.py

EXPOSE 42195

HEALTHCHECK --interval=5m CMD wget --spider -q http://localhost:42195 || exit 1

CMD python3 /app/server.py
