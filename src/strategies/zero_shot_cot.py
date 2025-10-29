import re
from src.models.base_model import BaseModel


def cot_prompt(question: str, llm: BaseModel) -> tuple[str, str]:
    prompt = f"""{question}

Let's think step by step.

First, let's identify what the hypothesis is asking.
Then, let's understand and examine each condition.
Let's trace and reason through the event sequences.
Finally, let's determine if the hypothesis can be satisfied.

Please reason through this problem thoroughly before answering.
The final answer must be either 'True' or 'False'."""

    llm.reconfig({'temperature': 0, 'max_tokens': 2000})

    response = llm.chat(message=prompt)

    # Extract answer - get the last occurrence
    pattern = r'(true|false)'
    matches = re.findall(pattern, response, re.IGNORECASE)
    answer = matches[-1].capitalize() if matches else None

    return response, answer
