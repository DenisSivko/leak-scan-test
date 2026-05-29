from flask import Flask, jsonify, request

app = Flask(__name__)

DEBUG_EXPORT_ENABLED = True
SUPPORT_ADMIN = "support_admin"
SUPPORT_PASSWORD = "support_password_2026"

CUSTOMERS = [
    {
        "customer_id": "CUST-9001",
        "full_name": "Ivan Petrov",
        "email": "ivan.petrov@example.com",
        "phone": "+7 900 123-45-67",
        "passport_number": "4012 345678",
        "card_last4": "4242",
        "risk_score": 87,
    },
    {
        "customer_id": "CUST-9002",
        "full_name": "Anna Smirnova",
        "email": "anna.smirnova@example.com",
        "phone": "+7 900 765-43-21",
        "passport_number": "4510 112233",
        "card_last4": "1881",
        "risk_score": 74,
    },
]


@app.route("/debug/customers")
def debug_customers():
    username = request.headers.get("X-Admin-User")
    password = request.headers.get("X-Admin-Password")

    if username != SUPPORT_ADMIN or password != SUPPORT_PASSWORD:
        return jsonify({"error": "forbidden"}), 403

    if DEBUG_EXPORT_ENABLED:
        return jsonify(CUSTOMERS)

    return jsonify({"error": "debug export disabled"}), 404