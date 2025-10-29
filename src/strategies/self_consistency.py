import re
from collections import Counter
from src.models.base_model import BaseModel


def self_consistency_prompt(question: str, llm: BaseModel, num_samples: int = 5) -> tuple[str, str]:
    llm.reconfig({'temperature': 0.7, 'max_tokens': 2000})

    prompt = question + """

Let's think step by step.

First, let's identify what the hypothesis is asking.
Then, let's understand and examine each condition.
Let's trace and reason through the event sequences.
Finally, let's determine if the hypothesis can be satisfied.

Please reason through this problem thoroughly before answering.
The final answer must be either 'True' or 'False'."""

    responses = []
    answers = []

    for i in range(num_samples):
        response = llm.chat(message=prompt)
        responses.append(response)

        # Extract answer - get the last occurrence
        pattern = r'(true|false)'
        matches = re.findall(pattern, response, re.IGNORECASE)
        if matches:
            answers.append(matches[-1].capitalize())

    # Majority voting
    if answers:
        vote_counts = Counter(answers)
        final_answer = vote_counts.most_common(1)[0][0]

        # Aggregate response info
        aggregated_response = f"Generated {num_samples} samples.\n"
        aggregated_response += f"Votes: {dict(vote_counts)}\n"
        aggregated_response += f"Final answer by majority vote: {final_answer}\n\n"
        aggregated_response += "Sample responses:\n" + "\n---\n".join(responses)
    else:
        final_answer = None
        aggregated_response = f"Failed to extract answers from {num_samples} samples.\n\n"
        aggregated_response += "Sample responses:\n" + "\n---\n".join(responses)

    return aggregated_response, final_answer