FROM public.ecr.aws/lambda/python:3.8

# https://serverfault.com/questions/683605/docker-container-time-timezone-will-not-reflect-changes
ENV TZ=America/Montreal
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# ${LAMBDA_TASK_ROOT} = /var/task
COPY /containers/data_prep/requirements.txt ${LAMBDA_TASK_ROOT} 

RUN pip install --no-cache-dir --upgrade -r requirements.txt

RUN mkdir -p /var/task/nltk_data

COPY /nltk_data /var/task/nltk_data

RUN mkdir -p /var/task/psycopg2

COPY /psycopg2 /var/task/psycopg2

COPY /services/data_prep ${LAMBDA_TASK_ROOT} 

CMD ["lambda_function.lambda_handler"]