import json
import logger

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

        pr = PullRequest(repo_name, pr_number, commit_sha)
        reviewer = LambdaReviewer()
        reviewer.review(pr)

        return {"statusCode": 200, "message": "ok"}
    except Exception as e:
        logger.error(f"Error processing order: {str(e)}")
        raise
