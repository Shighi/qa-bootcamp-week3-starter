# QA Bootcamp: Week 3 starter

This is your starting point for Week 3. Create your own copy with **Use this template**, then clone your copy.

## What's in here

| Folder | What it's for |
|---|---|
| `data/` | `shop.db`, a SQLite database for an online hardware shop (customers, products, orders, order_items). |
| `sql/` | Your SQL queries go here. |
| `python_basics/` | Your Python practice scripts go here. |
| `src/` | Code you will test: `chatbot/` (a returns-policy chatbot) and `agent/` (a customer-support agent). Treat both as black boxes: test them through their functions and don't read their code. |
| `tests/` | Your pytest tests. `test_setup.py` checks your environment is ready. |

## You need

Python 3.9 or newer. Check with `python3 --version` (on Windows: `python --version`).

## Set up

Create a virtual environment in the project folder:

```bash
python3 -m venv venv
```

Activate it.

Mac or Linux:

```bash
source venv/bin/activate
```

Windows:

```
venv\Scripts\activate
```

Install the packages:

```bash
pip install -r requirements.txt
```

## Run the tests

```bash
pytest
```

You should see `1 passed`. Because `pytest.ini` puts `src` on the path, your tests can import the code directly:

```python
from chatbot import ask, all_answers
from agent import run_agent
```
