FROM python:3.10-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set work directory
WORKDIR /code
# copy project
COPY . code/

COPY requirements.txt .
# install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt
# run app
CMD ["python", "main.py"]