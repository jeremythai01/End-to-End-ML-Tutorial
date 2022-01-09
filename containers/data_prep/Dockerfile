FROM public.ecr.aws/lambda/python:3.8


COPY /containers/data_prep/requirements.txt ${LAMBDA_TASK_ROOT} 

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY /services/data_prep ${LAMBDA_TASK_ROOT} 

COPY /services/utils ${LAMBDA_TASK_ROOT}/utils 

CMD ["lambda_function.lambda_handler"]