FROM python:3.8

WORKDIR /app

COPY . /app

RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile

EXPOSE 8050

CMD ["gunicorn", "-b", "0.0.0.0:8050", "app:app.server"]
