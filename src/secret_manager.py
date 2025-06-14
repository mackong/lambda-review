import json
import logging
import os

import boto3


class _SecretManager:
    def __init__(self, region: str = None):
        region = region or os.environ.get("AWS_REGION", "us-east-1")
        self.client = boto3.client(service_name="secretsmanager", region_name=region)

    def get_secret_string(self, name: str) -> str:
        """Get secret string from AWS secretsmanager.

        Fallback to corronsponding environment variable.
        """
        try:
            response = self.client.get_secret_value(SecretId=name)
            return json.loads(response["SecretString"])[name]
        except Exception as e:
            logging.error(f"failed to get secret string `{name}` from secretsmanager, error: {str(e)}")
            logging.warning(f"faillback to get secret string `{name}` from environment variabls")
            return os.environ.get(name.upper())

    def get_github_token(self) -> str:
        return self.get_secret_string("github_token")

    def get_openrouter_api_key(self) -> str:
        return self.get_secret_string("openrouter_api_key")


SecretManager = _SecretManager()
