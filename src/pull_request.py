from functools import cached_property

import github

from common import (
    GithubCommit, GithubFiles, GithubRepository,
    GithubPullRequest, GithubReviewComment,
)
from secret_manager import SecretManager


class PullRequest:
    def __init__(self, repo_name: str, pr_number: int, commit_sha: str):
        self.repo_name = repo_name
        self.pr_number = pr_number
        self.commit_sha = commit_sha

        github_token = SecretManager.get_github_token()
        self.github = github.Github(github_token)

    @cached_property
    def repo(self) -> GithubRepository:
        return self.github.get_repo(self.repo_name)

    @cached_property
    def pr(self) -> GithubPullRequest:
        return self.repo.get_pull(self.pr_number)

    @cached_property
    def commit(self) -> GithubCommit:
        return self.repo.get_commit(self.commit_sha)

    @cached_property
    def files(self) -> GithubFiles:
        return self.pr.get_files()

    def create_review(self, body: str, comments: list[GithubReviewComment]):
        self.pr.create_review(commit=self.commit, body=body, comments=comments)
