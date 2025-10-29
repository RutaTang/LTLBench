import re
from src.models.base_model import BaseModel


def few_shot_cot_prompt(question: str, llm: BaseModel) -> tuple[str, str]:
    prompt = """
=== Example 1 ===

Context:
Initially, event3 happened. After event3, either event1, or event2 must happen. After event1, either event2, or event3 must happen. After event2, event3 must happen.

Hypothesis:
C1: Event1 happens or event3 happens.
C2: Event1 happens or C1 holds.
C3: C2 eventually holds.

Let's think step by step:
1. We need to check if C3 (C2 eventually holds) is true.
2. C2 is: Event1 happens or C1 holds
3. C1 is: Event1 happens or event3 happens
4. So C2 simplifies to: Event1 happens or (Event1 happens or event3 happens)
5. This is logically equivalent to: Event1 happens or event3 happens
6. The initial state has event3 = true
7. Therefore, C2 holds at the initial state (since event3 is true)
8. Since C2 holds at the initial state, C3 (C2 eventually holds) is True

Answer: True

=== Example 2 ===

Context:
Initially, event2 happened. After event2, event3 must happen. After event3, no other events can happen. After event1, either event2, or event3 must happen.

Hypothesis:
C1: Event2 happens and event3 happens.
C2: C1 holds in the next state.
C3: C2 eventually holds.

Let's think step by step:
1. We need to check if C3 (C2 eventually holds) is true.
2. C2 is: C1 holds in the next state, where C1 is (event2 AND event3)
3. For C1 to be true, both event2 and event3 must be true simultaneously
4. In any single state, only one event can be true at a time
5. Starting from event2, the next state must be event3
6. From event3, it stays at event3 (no other events can happen)
7. At no point can event2 and event3 be true simultaneously in the same state
8. Therefore, C1 is always false
9. If C1 is always false, then C2 (C1 in the next state) is always false
10. If C2 is always false, then C3 (C2 eventually holds) is False

Answer: False

=== Now solve this problem ===

""" + question + """

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