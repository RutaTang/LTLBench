import re
from src.models.base_model import BaseModel


def direct_prompt(question: str, llm: BaseModel) -> tuple[str, str]:
    prompt = f"{question}\n\nThe answer must be either 'True' or 'False'."

    llm.reconfig({'temperature': 0, 'max_tokens': 2000})

    response = llm.chat(message=prompt)

    # Extract answer - get the last occurrence
    pattern = r'(true|false)'
    matches = re.findall(pattern, response, re.IGNORECASE)
    answer = matches[-1].capitalize() if matches else None

    return response, answer
