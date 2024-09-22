FROM python:3.12

RUN pip install --upgrade pip && pip install garth flask

COPY server.py /app/server.py
CMD python /app/server.py
