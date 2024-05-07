FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED=1
WORKDIR /sat_proj
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ("python3", "manage.py" ,"runserver")
