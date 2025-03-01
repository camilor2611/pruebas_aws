from typing import Dict
from aws_cdk import (
    Stack,
    Duration,
    aws_iam as iam,
    aws_s3 as s3,
    aws_s3_notifications as s3n
)
from constructs import Construct
from aws_cdk.aws_lambda import DockerImageFunction, DockerImageCode


class StackLambdas(Stack):
    def __init__(self, scope: Construct, id: str, context: Dict, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self.load_file(context)
        self.generate_check_sum(context)
        self.get_check_sum(context)

    def load_file(self, context: Dict):
        prefix_app_load_file = "load_file"
        lambda_load_file_role = iam.Role(self, f"{context["ENVIRONMENT"]}{prefix_app_load_file}",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole")
            ]
        )

        lambda_load_file_role.add_to_policy(iam.PolicyStatement(
            actions=["s3:PutObject"],
            resources=[f"arn:aws:s3:::{context['BUCKET_NAME']}/*"]
        ))

        lambda_load_file_role.add_to_policy(iam.PolicyStatement(
            actions=["dynamodb:GetItem", "dynamodb:Query"],
            resources=[f"arn:aws:dynamodb:{context['AWS_REGION_DEPLOY']}:{context['AWS_ACCOUNT_DEPLOY']}:table/{context['DYNAMO_TABLE_NAME']}"]
        ))

        docker_image = DockerImageCode.from_image_asset(directory=prefix_app_load_file, file="Dockerfile")

        # Crear la función Lambda
        DockerImageFunction(self, f"{context["ENVIRONMENT"]}_{prefix_app_load_file}",
            code=docker_image,
            role=lambda_load_file_role,
            timeout=Duration.seconds(30),
            function_name=f"{context["ENVIRONMENT"]}_{prefix_app_load_file}",
            environment=context,
            memory_size=3008
        )


    def generate_check_sum(self, context: Dict):
        prefix_app_generate_check_sum = "generate_check_sum"

        bucket = s3.Bucket.from_bucket_name(self, "ExistingBucket", context['BUCKET_NAME'])
        lambda_generate_check_sum_role = iam.Role(self, f"{context["ENVIRONMENT"]}{prefix_app_generate_check_sum}",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole")
            ]
        )

        lambda_generate_check_sum_role.add_to_policy(iam.PolicyStatement(
            actions=["s3:GetObject"],
            resources=[f"arn:aws:s3:::{context['BUCKET_NAME']}/*"]
        ))

        lambda_generate_check_sum_role.add_to_policy(iam.PolicyStatement(
            actions=["dynamodb:PutItem"],
            resources=[f"arn:aws:dynamodb:{context['AWS_REGION_DEPLOY']}:{context['AWS_ACCOUNT_DEPLOY']}:table/{context['DYNAMO_TABLE_NAME']}"]
        ))

        docker_image = DockerImageCode.from_image_asset(directory=prefix_app_generate_check_sum, file="Dockerfile")

        # Crear la función Lambda
        app_generate_check_sum_lambda = DockerImageFunction(self, f"{context["ENVIRONMENT"]}_{prefix_app_generate_check_sum}",
            code=docker_image,
            role=lambda_generate_check_sum_role,
            timeout=Duration.seconds(30),
            function_name=f"{context["ENVIRONMENT"]}_{prefix_app_generate_check_sum}",
            environment=context,
            memory_size=3008
        )

        bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED,
            s3n.LambdaDestination(app_generate_check_sum_lambda)
        )

    def get_check_sum(self, context: Dict):
        prefix_check_sum = "get_check_sum"
        lambda_check_sum = iam.Role(self, f"{context["ENVIRONMENT"]}{prefix_check_sum}",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole")
            ]
        )

        lambda_check_sum.add_to_policy(iam.PolicyStatement(
            actions=["dynamodb:GetItem", "dynamodb:Query"],
            resources=[f"arn:aws:dynamodb:{context['AWS_REGION_DEPLOY']}:{context['AWS_ACCOUNT_DEPLOY']}:table/{context['DYNAMO_TABLE_NAME']}"]
        ))

        docker_image = DockerImageCode.from_image_asset(directory=prefix_check_sum, file="Dockerfile")

        # Crear la función Lambda
        DockerImageFunction(self, f"{context["ENVIRONMENT"]}_{prefix_check_sum}",
            code=docker_image,
            role=lambda_check_sum,
            timeout=Duration.seconds(30),
            function_name=f"{context["ENVIRONMENT"]}_{prefix_check_sum}",
            environment=context,
            memory_size=3008
        )
