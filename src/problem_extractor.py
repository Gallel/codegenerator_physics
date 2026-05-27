import json
import os
import time
from openai import OpenAI
from src.settings import EXTRACTION_PROMPT, OPENAI_MODEL, OPENAI_TEMPERATURE
from src.metrics import get_collector
from src.metrics.efficiency import LAYER_EXTRACT

LLM_CALL_DELAY = float(os.getenv("LLM_CALL_DELAY", "3.0"))

def extract_problem_goals(task_text: str) -> dict:
    client = OpenAI(max_retries=8)

    if LLM_CALL_DELAY > 0:
        time.sleep(LLM_CALL_DELAY)

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": EXTRACTION_PROMPT},
            {"role": "user", "content": f"PROBLEM TEXT:\n{task_text}"}
        ],
        temperature=OPENAI_TEMPERATURE,
    )

    # Token usage for the extraction call (run_benchmark may copy these
    # totals into the per-branch collectors to honour the paired-sampling
    # cost attribution).
    col = get_collector()
    if col is not None and getattr(response, "usage", None) is not None:
        col.record_tokens(
            LAYER_EXTRACT,
            getattr(response.usage, "prompt_tokens", 0),
            getattr(response.usage, "completion_tokens", 0),
        )

    text_content = response.choices[0].message.content.strip()
    if text_content.startswith("```json"):
        text_content = text_content[7:]
    if text_content.endswith("```"):
        text_content = text_content[:-3]
    return json.loads(text_content.strip())
