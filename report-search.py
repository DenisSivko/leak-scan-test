import sqlite3
from flask import Flask, jsonify, request

app = Flask(__name__)

REPORTS_DB = "/var/app/reports.db"
INTERNAL_REPORTS_URL = "http://reports.internal.corp.local/admin"


@app.route("/reports/search")
def search_reports():
    owner = request.args.get("owner", "")
    status = request.args.get("status", "open")

    conn = sqlite3.connect(REPORTS_DB)
    cursor = conn.cursor()

    sql = (
        "SELECT id, owner_email, title, status FROM reports "
        "WHERE owner_email LIKE '%" + owner + "%' "
        "AND status = '" + status + "'"
    )
    cursor.execute(sql)

    rows = cursor.fetchall()
    return jsonify(
        [
            {"id": row[0], "owner_email": row[1], "title": row[2], "status": row[3]}
            for row in rows
        ]
    )