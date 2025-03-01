from dotenv import load_dotenv
load_dotenv("../.env")
import os

from aws_cdk import App, Environment, DefaultStackSynthesizer
from stack import StackLambdas

app = App()


context = {
    "ENVIRONMENT": os.environ.get("ENVIRONMENT"),
    "AWS_ACCOUNT_DEPLOY": os.environ.get("AWS_ACCOUNT_DEPLOY"),
    "AWS_REGION_DEPLOY": os.environ.get("AWS_REGION_DEPLOY"),
    "BUCKET_NAME": os.environ.get("BUCKET_NAME"),
    "QUALIFIER": os.environ.get("QUALIFIER"),
    "DYNAMO_TABLE_NAME": os.environ.get("DYNAMO_TABLE_NAME"),
}

synthesizer = DefaultStackSynthesizer(
    qualifier=context['QUALIFIER']
)

environment_obj = Environment(account=context['AWS_ACCOUNT_DEPLOY'], region=context['AWS_REGION_DEPLOY'])

stack = StackLambdas(
    app,
    f"{context['ENVIRONMENT']}StackLambdas",
    context,
    env=environment_obj,
    synthesizer=synthesizer
)

app.synth()
