from pathlib import Path

MIN_CHARS = 260_000
output = Path("large-leak-fixture.py")

header = '''\
import sqlite3
import subprocess
from flask import Flask, jsonify, request

app = Flask(__name__)

DATABASE_CONFIG = {
    "host": "10.50.12.8",
    "port": 5432,
    "database": "billing",
    "user": "billing_admin",
    "password": "billing_password_2026_large_fixture"
}

DEPLOY_TOKEN = "HARDCODED_DEPLOY_TOKEN_LARGE_FIXTURE_7f4a9c2b8e1d4a6f"

@app.route("/health")
def health():
    return jsonify({"status": "ok"})
'''

middle_risk = '''\

@app.route("/reports/search")
def search_reports():
    owner = request.args.get("owner", "")
    status = request.args.get("status", "open")

    conn = sqlite3.connect("/var/app/reports.db")
    cursor = conn.cursor()

    sql = (
        "SELECT id, owner_email, title, status FROM reports "
        "WHERE owner_email LIKE '%" + owner + "%' "
        "AND status = '" + status + "'"
    )
    cursor.execute(sql)

    return jsonify(cursor.fetchall())
'''

end_risk = '''\

INTERNAL_ADMIN_URL = "http://admin-api.internal.corp.local"

FEATURE_FLAGS = {
    "debug_mode": True,
    "allow_admin_impersonation": True,
    "audit_log_enabled": False,
    "verify_tls": False,
}

CUSTOMER_EXPORT = [
    {
        "customer_id": "CUST-9901",
        "full_name": "Ivan Petrov",
        "email": "ivan.petrov@example.com",
        "passport_number": "4012 345678",
        "card_last4": "4242",
    },
    {
        "customer_id": "CUST-9902",
        "full_name": "Anna Smirnova",
        "email": "anna.smirnova@example.com",
        "passport_number": "4510 112233",
        "card_last4": "1881",
    },
]

@app.route("/admin/backup")
def run_backup():
    dataset = request.args.get("dataset", "daily")
    archive_name = request.args.get("archive", "backup")
    command = f"tar -czf /tmp/{archive_name}.tgz /var/app/data/{dataset}"
    subprocess.check_output(command, shell=True)

    return jsonify({"status": "started", "admin_url": INTERNAL_ADMIN_URL})
'''

def filler_block(index: int) -> str:
    return f'''

def harmless_transform_{index}(value):
    normalized = str(value).strip().lower()
    if normalized in {{"none", "null", "undefined"}}:
        return None
    result = {{
        "index": {index},
        "value": normalized,
        "source": "large-fixture",
        "description": "regular application code used to increase file size without adding extra risks"
    }}
    return result
'''

parts = [header]
index = 0

while sum(len(part) for part in parts) < 90_000:
    parts.append(filler_block(index))
    index += 1

parts.append(middle_risk)

while sum(len(part) for part in parts) < 180_000:
    parts.append(filler_block(index))
    index += 1

parts.append(end_risk)

while sum(len(part) for part in parts) < MIN_CHARS:
    parts.append(filler_block(index))
    index += 1

content = "".join(parts)
output.write_text(content, encoding="utf-8")

print(f"written: {output}")
print(f"chars: {len(content)}")
print(f"bytes: {len(content.encode('utf-8'))}")
print(f"filler_functions: {index}")