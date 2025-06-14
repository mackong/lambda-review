import json
import logging

from lambda_reviewer import LambdaReviewer
from pull_request import PullRequest


def lambda_handler(event, context):
    if 'body' not in event:
        return {"statusCode": 400, "message": "no body found"}

    try:
        payload = json.loads(event['body'])

        repo_name = payload["repository"]["full_name"]
        pr_number = payload["pull_request"]["number"]
        commit_sha = payload["pull_request"]["head"]["sha"]

        logging.info(f"review for pr-{pr_number} of {repo_name}")

        pr = PullRequest(repo_name, pr_number, commit_sha)
        reviewer = LambdaReviewer()
        reviewer.review(pr)

        logging.info(f"pr-{pr_number} of {repo_name} reviewed successful")

        return {"statusCode": 200, "message": "ok"}
    except Exception as e:
        logging.error(f"Error processing pull request: {str(e)}")
        raise
