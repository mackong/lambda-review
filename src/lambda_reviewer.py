import os
import textwrap

from common import GithubFile, LLMReviewIssue, SUPPORTED_LANGS
from llm import ReviewLLM
from pull_request import PullRequest


class LambdaReviewer:
    def __init__(self):
        self.llm = ReviewLLM()

    def review(self, pr: PullRequest):
        files = [f for f in pr.files if self._is_supported_file(f.filename)]
        diff = self._build_commit_diff(files)
        resp = self.llm.review(diff)
        issues = resp.issues

        comments = [{
            "path": issue.file,
            "line": issue.line,
            "body": self._build_comment_body(issue)
        } for issue in issues]
        pr.create_review(body="LambdaReview Report", comments=comments)

    def _get_file_lang(self, fname: str) -> str:
        _, ext = os.path.splitext(fname)
        return SUPPORTED_LANGS.get(ext, "")

    def _is_supported_file(self, fname) -> bool:
        return self._get_file_lang(fname) != ""

    def _build_commit_diff(self, files: list[GithubFile]) -> str:
        diffs = [
            f"File: {f.filename}\n{f.patch}"
            for f in files
        ]
        return "\n\n".join(diffs)

    def _build_comment_body(self, issue: LLMReviewIssue) -> str:
        return f"""# {issue.category}
{issue.description}

# Fix
{issue.fix_desc}

```{self._get_file_lang(issue.file)}
{textwrap.dedent(issue.fix_code)}
```"""


if __name__ == "__main__":
    repo_name = "mackong/lambda-review-demo"
    pr_number = 1
    commit_sha = "804e6c2429e01f877aa2d7a43eb7fcd385eaf11c"
    pr = PullRequest(repo_name, pr_number, commit_sha)
    reviewer = LambdaReviewer()
    reviewer.review(pr)
