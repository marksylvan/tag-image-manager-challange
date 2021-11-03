#!/usr/bin/env python3
import os
import typing

import boto3


def do_login(
    client_id: str, username: str, password: str
) -> typing.Dict[str, typing.Any]:
    """Does a Cognito IDP login and returns the auth token"""
    client = boto3.client("cognito-idp")
    response = client.initiate_auth(
        AuthFlow="USER_PASSWORD_AUTH",
        AuthParameters={"USERNAME": username, "PASSWORD": password},
        ClientId=client_id,
    )
    return response


def get_id_token() -> str:
    client_id = os.environ["COGNITO_CLIENT_ID"]
    username = os.environ["COGNITO_USERNAME"]
    password = os.environ["COGNITO_PASSWORD"]

    res = do_login(client_id, username, password)

    challenge_name = res.get("ChallengeName", None)

    if challenge_name is not None:
        raise ValueError(
            f"Unable to login to account, status is {challenge_name}"
        )

    return res["AuthenticationResult"]["IdToken"]


if __name__ == "__main__":
    print(get_id_token(), end="")
