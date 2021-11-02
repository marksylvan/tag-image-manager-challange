from os import environ

from chalice.app import CognitoUserPoolAuthorizer

cognito_authorizer = CognitoUserPoolAuthorizer(
    "CognitoAuthorizer",
    provider_arns=[environ["COGNITO_POOL_ARN"]],
)
