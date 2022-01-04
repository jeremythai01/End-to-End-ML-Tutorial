FROM python:3.9

WORKDIR /data_scrape

COPY /containers/data_scrape/requirements.txt /data_scrape/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /data_scrape/requirements.txt

COPY /services/data_scrape /data_scrape

CMD ["python", "lambda_function.py"]