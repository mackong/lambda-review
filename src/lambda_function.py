import json

from lambda_reviewer import LambdaReviewer
from pull_request import PullRequest


def lambda_handler(event, context):
    if 'body' not in event:
        print("no body found in event")
        return {"statusCode": 400, "message": "no body found"}

    try:
        payload = json.loads(event['body'])

        action = payload["action"]
        if action not in ("opened", "reopened"):
            print("invalid action", action)
            return {"statusCode": 200, "message": "ok"}

        repo_name = payload["repository"]["full_name"]
        pr_number = payload["pull_request"]["number"]
        commit_sha = payload["pull_request"]["head"]["sha"]

        print(f"review for pr-{pr_number} of {repo_name}")

        pr = PullRequest(repo_name, pr_number, commit_sha)
        reviewer = LambdaReviewer()
        reviewer.review(pr)

        print(f"pr-{pr_number} of {repo_name} reviewed successful")

        return {"statusCode": 200, "message": "ok"}
    except Exception as e:
        print(f"Error processing pull request: {str(e)}")
        raise
