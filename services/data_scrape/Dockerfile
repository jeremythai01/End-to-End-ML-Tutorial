FROM python:3.9

WORKDIR /data_scrape

COPY requirements.txt /data_scrape/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /data_scrape/requirements.txt

COPY ./app /data_scrape/app

CMD ["python", "app/lambda_function.py"]