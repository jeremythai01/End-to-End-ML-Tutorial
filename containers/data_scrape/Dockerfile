FROM public.ecr.aws/lambda/python:3.8

# https://serverfault.com/questions/683605/docker-container-time-timezone-will-not-reflect-changes
ENV TZ=America/Montreal
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# ${LAMBDA_TASK_ROOT} = /var/task
COPY /containers/data_scrape/requirements.txt ${LAMBDA_TASK_ROOT} 

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY /services/data_scrape ${LAMBDA_TASK_ROOT} 

CMD ["lambda_function.lambda_handler"]