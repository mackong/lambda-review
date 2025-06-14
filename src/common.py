from typing import List, Literal

import github
from pydantic import BaseModel, Field

# Shorten types for github types.
type GithubCommit = github.Commit.Commit
type GithubFile = github.File.File
type GithubPaginatedList = github.PaginatedList.PaginatedList
type GithubPullRequest = github.PullRequest.PullRequest
type GithubRepository = github.Repository.Repository
type GithubReviewComment = github.PullRequest.ReviewComment

type GithubFiles = GithubPaginatedList[GithubFile]

# Supported programming languages
SUPPORTED_LANGS = {
    ".c": "c",
    ".cxx": "cpp",
    ".go": "go",
    ".java": "java",
    ".js": "javascript",
    ".py": "python",
    ".rb": "ruby",
}


class LLMReviewIssue(BaseModel):
    category: Literal["Error", "Warning", "Security", "Refactor", "Performance"] = Field(
        ...,
        description="The category of the issue"
    )
    file: str = Field(
        ...,
        description="The source code file of the issue"
    )
    line: int = Field(
        ...,
        description="The source code line of the issue"
    )
    description: str = Field(
        ...,
        description="The detailed description of the issue"
    )
    fix_desc: str = Field(
        ...,
        description="The description of fix solution for the issue"
    )
    fix_code: str = Field(
        ...,
        description="The code of fix solution for the issue"
    )


class LLMReviewResponse(BaseModel):
    issues: List[LLMReviewIssue] = Field(
        ...,
        description="issues of the diff"
    )
