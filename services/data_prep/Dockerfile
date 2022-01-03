FROM python:3.9

WORKDIR /data_prep

COPY requirements.txt /data_prep/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /data_prep/requirements.txt

COPY ./app /data_prep/app

CMD ["python", "app/lambda_function.py"]