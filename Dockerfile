FROM python:3.6-slim

ARG app_dir='/opt/vkservices'
ENV PYTHONBUFFERED=0

WORKDIR ${app_dir}

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "manage.py", "runserver", "--port", "80"]