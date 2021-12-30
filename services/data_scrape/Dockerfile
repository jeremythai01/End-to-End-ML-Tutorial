FROM tiangolo/uvicorn-gunicorn:python3.8

WORKDIR /data_scrape

COPY requirements.txt /data_scrape/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /data_scrape/requirements.txt

COPY ./app /data_scrape/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "420"]