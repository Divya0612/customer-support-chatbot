import json
import os

from mock_data import ORDERS as _SEED_ORDERS

ORDERS_FILE = "orders.json"


def _load_orders():
    if os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE) as f:
            return json.load(f)
    return {k: dict(v) for k, v in _SEED_ORDERS.items()}


def _save_orders(orders):
    with open(ORDERS_FILE, "w") as f:
        json.dump(orders, f, indent=4)


ORDERS = _load_orders()


def track_order(order_id: str) -> str:
    order = ORDERS.get(order_id.upper())
    if not order:
        return f"No order found with ID {order_id}. Please check the order ID and try again."

    status_map = {
        "processing": "Your order is being processed at our warehouse.",
        "shipped": "Your order has been shipped and is on its way.",
        "out_for_delivery": "Your order is out for delivery.",
        "delivered": "Your order has been delivered.",
        "cancelled": "Your order has been cancelled.",
    }
    status_text = status_map.get(order["status"], order["status"])
    return (
        f"Order {order_id.upper()}: {order['item']}\n"
        f"Status: {status_text}\n"
        f"Delivery: {order['expected_delivery']}"
    )


def cancel_order(order_id: str) -> str:
    order = ORDERS.get(order_id.upper())
    if not order:
        return f"No order found with ID {order_id}. Please check the order ID and try again."

    if not order["cancellable"]:
        return (
            f"Order {order_id.upper()} cannot be cancelled because it has already been {order['status']}. "
            f"You may return the item after delivery as per our return policy."
        )

    order["status"] = "cancelled"
    order["cancellable"] = False
    _save_orders(ORDERS)
    return (
        f"Order {order_id.upper()} ({order['item']}) has been successfully cancelled. "
        f"A refund of Rs. {order['amount']} will be processed to your original payment method within 5-7 business days."
    )


def check_refund_status(order_id: str) -> str:
    order = ORDERS.get(order_id.upper())
    if not order:
        return f"No order found with ID {order_id}. Please check the order ID and try again."

    if not order["refund_status"]:
        return f"There is no refund currently associated with order {order_id.upper()}."

    status_map = {
        "initiated": "Your refund has been initiated and is currently under review.",
        "processing": "Your refund is being processed by our finance team.",
        "processed": (
            f"Your refund of Rs. {order['amount']} has been processed. "
            f"It should reflect in your account within 5-7 business days."
        ),
        "completed": f"Your refund of Rs. {order['amount']} has been successfully credited to your account.",
    }
    return status_map.get(order["refund_status"], f"Refund status: {order['refund_status']}")


def connect_human_agent() -> str:
    return (
        "Your conversation has been flagged for human support. "
        "A Customer Support support specialist will reach out to you within 24 hours "
        "via your registered email or phone number. "
        "You can also call us directly at +91-1800-123-4567 (Mon-Sat, 9 AM - 7 PM IST)."
    )
