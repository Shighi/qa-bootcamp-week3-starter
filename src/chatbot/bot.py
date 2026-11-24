"""A mock returns-policy chatbot for the Week 3 AI testing exercise.

Treat it as a black box. It stands in for an AI service you cannot see inside,
so test it through ask() and all_answers(), and don't go looking for the
"right" answers in the data file.
"""
import json
import random
from pathlib import Path
from typing import Optional

_DATA = json.loads((Path(__file__).parent / "answers.json").read_text(encoding="utf-8"))

# How likely each variant is when the bot is asked at random.
_WEIGHT_BY_SUFFIX = {"a": 0.4, "b": 0.3, "c": 0.15, "d": 0.15}

_FALLBACK = "Sorry, I can only answer questions about our returns policy."


def _normalise(text: str) -> str:
    return " ".join(text.lower().split()).rstrip("?!. ")


_BY_QUESTION = {}
for _item in _DATA:
    _BY_QUESTION.setdefault(_normalise(_item["question"]), []).append(_item)

# The five questions, in order.
QUESTIONS = []
for _item in _DATA:
    if _item["question"] not in QUESTIONS:
        QUESTIONS.append(_item["question"])
QUESTIONS.sort(key=lambda q: next(i["id"] for i in _DATA if i["question"] == q))


def ask(question: str, seed: Optional[int] = None) -> str:
    """Return one answer to the question, chosen at random.

    With a seed, the same question always gets the same answer.
    """
    items = _BY_QUESTION.get(_normalise(question))
    if not items:
        return _FALLBACK
    rng = random.Random(seed) if seed is not None else random
    weights = [_WEIGHT_BY_SUFFIX[item["id"][-1]] for item in items]
    return rng.choices(items, weights=weights, k=1)[0]["answer"]


def all_answers() -> list:
    """Return every answer the bot can give: a list of dicts with id, question and answer."""
    return [dict(item) for item in _DATA]
