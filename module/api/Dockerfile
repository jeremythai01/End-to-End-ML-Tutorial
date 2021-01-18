FROM python:3.8

WORKDIR /app

COPY . /app

RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile

EXPOSE 5000

ENTRYPOINT [ "python3" ]
CMD ["app.py"]
