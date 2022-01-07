FROM public.ecr.aws/lambda/python:3.8


COPY /containers/ml_predict/requirements.txt ${LAMBDA_TASK_ROOT} 

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY /services/ml_predict ${LAMBDA_TASK_ROOT} 

CMD ["lambda_function.lambda_handler"]