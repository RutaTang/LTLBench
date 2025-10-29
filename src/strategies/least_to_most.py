import re
from src.models.base_model import BaseModel


def least_to_most_prompt(question: str, llm: BaseModel) -> tuple[str, str]:
    llm.reconfig({'temperature': 0, 'max_tokens': 2000})

    # Step 1: Break down the problem into subproblems
    breakdown_prompt = question + """

Let me break this down into smaller, manageable parts:

1. What events are involved and what are the initial conditions?
2. What are the transition rules between events?
3. What does each sub-condition (C1, C2, C3, etc.) mean?
4. How do these conditions relate to each other?

Please answer each of these questions step by step."""

    breakdown_response = llm.chat(message=breakdown_prompt)

    # Step 2: Solve the main problem using the breakdown
    solve_prompt = question + f"""

Based on the following breakdown of the problem:

{breakdown_response}

Now, let's use this understanding to solve the main problem step by step:

1. Start with the simplest conditions and work up to the complex ones
2. Trace through the event sequences
3. Check if the final hypothesis can be satisfied

The final answer must be either 'True' or 'False'."""

    final_response = llm.chat(message=solve_prompt)

    # Extract answer - get the last occurrence
    pattern = r'(true|false)'
    matches = re.findall(pattern, final_response, re.IGNORECASE)
    answer = matches[-1].capitalize() if matches else None

    # Combine both responses
    full_response = f"=== Step 1: Problem Breakdown ===\n{breakdown_response}\n\n"
    full_response += f"=== Step 2: Solution ===\n{final_response}"

    return full_response, answer