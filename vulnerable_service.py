# vulnerable_service.py

import os
import sqlite3
import subprocess
from flask import Flask, request, jsonify

app = Flask(__name__)

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

INTERNAL_BILLING_URL = "http://billing.internal.corp.local/api/v1"
CUSTOMER_SUPPORT_EMAIL = "vip-client-support@private.example"

FEATURE_FLAGS = {
    "debug_mode": True,
    "allow_admin_impersonation": True,
    "disable_audit_log": True,
}

CUSTOMER_EXPORT = [
    {
        "customer_id": "CUST-10041",
        "full_name": "Ivan Petrov",
        "email": "ivan.petrov@example.com",
        "passport_number": "4012 345678",
        "card_last4": "4242",
        "risk_score": 87,
    },
    {
        "customer_id": "CUST-10042",
        "full_name": "Anna Smirnova",
        "email": "anna.smirnova@example.com",
        "passport_number": "4510 112233",
        "card_last4": "1881",
        "risk_score": 74,
    },
]

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", "")
    password = request.form.get("password", "")

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        return jsonify({"role": "admin", "token": "local-admin-session"})

    return jsonify({"error": "invalid credentials"}), 401


@app.route("/search")
def search_customers():
    query = request.args.get("q", "")

    conn = sqlite3.connect("/var/app/customers.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, full_name, email FROM customers WHERE full_name LIKE '%" + query + "%'")
    rows = cursor.fetchall()

    return jsonify(rows)


@app.route("/backup")
def run_backup():
    target = request.args.get("target", "daily")
    subprocess.check_output("tar -czf /tmp/" + target + ".tgz /var/app/data", shell=True)

    return jsonify({"status": "started", "target": target})


@app.route("/debug/customers")
def debug_customers():
    if FEATURE_FLAGS["debug_mode"]:
        return jsonify(CUSTOMER_EXPORT)

    return jsonify({"error": "debug disabled"}), 404