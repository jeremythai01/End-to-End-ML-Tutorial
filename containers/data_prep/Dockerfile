FROM python:3.9

WORKDIR /data_prep

COPY /containers/data_prep/requirements.txt /data_prep/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /data_prep/requirements.txt

COPY /services/data_prep /data_prep

CMD ["python", "lambda_function.py"]