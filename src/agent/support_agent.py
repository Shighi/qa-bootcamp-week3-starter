"""A mock customer-support agent for the Week 3 AI testing exercise.

Treat it as a black box. It stands in for an AI agent you cannot see inside,
so test it through run_agent() and don't read the code to find what is wrong.

run_agent(request) returns what the agent did:
    {
      'tool_calls': [{'name': ..., 'args': {...}}, ...],
      'final_answer': '...',
      'orders': {'1001': 'cancelled', ...},   # status of every order afterwards
    }
"""
import re

_START_ORDERS = {1001: "pending", 1002: "pending", 1003: "pending", 2001: "delivered", 2002: "delivered"}


class _Run:
    """One run of the agent, with its own copy of the orders."""

    def __init__(self):
        self.orders = dict(_START_ORDERS)
        self.calls = []

    def call(self, name, **args):
        self.calls.append({"name": name, "args": dict(args)})
        return getattr(self, "_" + name)(**args)

    def _get_order(self, order_id):
        return {"order_id": order_id, "status": self.orders[order_id]}

    def _cancel_order(self, order_id):
        if self.orders[order_id] == "pending":
            self.orders[order_id] = "cancelled"
            return {"ok": True}
        return {"ok": False, "error": "only pending orders can be cancelled"}

    def _issue_refund(self, order_id, amount):
        if not isinstance(amount, (int, float)):
            return {"ok": False, "error": "amount must be a number"}
        self.orders[order_id] = "refunded"
        return {"ok": True}

    def _send_email(self, order_id, message):
        return {"ok": True}


def _cancel_1001(run):
    run.call("get_order", order_id=1001)
    run.call("cancel_order", order_id=1001)
    return "Order 1001 has been cancelled."


def _cancel_1002(run):
    for _ in range(3):
        run.call("get_order", order_id=1002)
    for _ in range(2):
        run.call("send_email", order_id=1002, message="Checking your order.")
    run.call("cancel_order", order_id=1002)
    return "Order 1002 has been cancelled. I've emailed you to confirm."


def _refund_2001(run):
    run.call("get_order", order_id=2001)
    run.call("issue_refund", order_id=2001, amount="80")
    return "I've refunded $80.00 for order 2001."


def _cancel_2002(run):
    run.call("get_order", order_id=2002)
    run.call("issue_refund", order_id=2002, amount=55.0)
    return "No problem, order 2002 has been cancelled."


def _status_1003(run):
    run.call("get_order", order_id=1003)
    run.call("cancel_order", order_id=1003)
    return "Order 1003 is pending."


def _normalise(text):
    return " ".join(re.sub(r"[^a-z0-9 ]", " ", text.lower()).split())


_SCENARIOS = {
    _normalise("Cancel order 1001"): _cancel_1001,
    _normalise("Cancel order 1002"): _cancel_1002,
    _normalise("Refund order 2001, it arrived broken"): _refund_2001,
    _normalise("Cancel order 2002"): _cancel_2002,
    _normalise("What is the status of order 1003?"): _status_1003,
}


def run_agent(request):
    """Run the agent on a request written in plain English and return what it did."""
    run = _Run()
    scenario = _SCENARIOS.get(_normalise(request))
    if scenario is None:
        final_answer = "Sorry, I can't help with that."
    else:
        final_answer = scenario(run)
    return {
        "tool_calls": run.calls,
        "final_answer": final_answer,
        "orders": {str(order_id): status for order_id, status in run.orders.items()},
    }
