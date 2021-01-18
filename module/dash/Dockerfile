FROM python:3.8

WORKDIR /app

COPY . /app

RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile

EXPOSE 8050

ENTRYPOINT [ "python3" ]
CMD ["dash_app.py"]
