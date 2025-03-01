FROM public.ecr.aws/lambda/python:3.12

COPY requirements.txt ${LAMBDA_TAKS_ROOT}
RUN pip install -r requirements.txt

COPY ./ ${LAMBDA_TAKS_ROOT}
CMD [ "app.handler" ]
