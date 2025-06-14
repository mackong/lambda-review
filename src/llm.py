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
        template = f"""You are a senior software engineer performing a code review.

Please analyze the following Git diff and provide suggestions for:

1. **Errors** – logic bugs, missing checks, obvious mistakes
2. **Warnings** – code smells, risky patterns, deprecated usage
3. **Refactor Suggestions** – opportunities to improve structure, clarity
4. **Security Issues** - SQL injection, headcoded secrets
5. **Performance Issues** - 1+n queries, memory leaks

Here is the Git diffs:

```
{diff}
```
"""
        return template.strip()
