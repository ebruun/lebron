FROM python:3.7

COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /code
COPY . /code

EXPOSE 5000

CMD ["gunicorn", "app:app", "--reload", "-b", "0.0.0.0:5000"]
