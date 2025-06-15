import os

import instructor
from openai import OpenAI

from common import LLMReviewResponse
from secret_manager import SecretManager


class ReviewLLM:
    def __init__(self):
        api_key = SecretManager.get_openrouter_api_key()
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )
        self.client = instructor.from_openai(client)
        self.model = os.environ.get(
            "OPENROUTER_MODEL", "anthropic/claude-3-7-sonnet-20250219"
        )

    def review(self, diff: str) -> LLMReviewResponse:
        prompt = self._build_prompt(diff)
        return self.client.chat.completions.create(
            model=self.model,
            response_model=LLMReviewResponse,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

    def _build_prompt(self, diff: str) -> str:
        template = f"""You are a senior software engineer performing a thorough code review. Analyze the provided Git diff and identify:

1. **Errors** – Logic bugs, missing null/type checks, incorrect calculations, state issues
2. **Warnings** – Code smells, anti-patterns, tech debt, deprecated APIs, risky practices
3. **Refactor Suggestions** – Duplicate code, complex methods, poor structure, unclear naming
4. **Security Issues** - Injection risks, auth issues, data exposure, hardcoded secrets
5. **Performance Issues** - Inefficient algorithms, N+1 queries, memory leaks, blocking ops

Here is the Git diffs:

```
{diff}
```
"""
        return template.strip()
