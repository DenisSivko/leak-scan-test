import subprocess
from flask import Flask, jsonify, request

app = Flask(__name__)

BACKUP_ROOT = "/var/app/data"
BACKUP_BUCKET = "s3://prod-billing-backups-private"


@app.route("/admin/backup")
def run_backup():
    dataset = request.args.get("dataset", "daily")
    archive_name = request.args.get("archive", "backup")

    archive_path = f"/tmp/{archive_name}.tgz"
    command = f"tar -czf {archive_path} {BACKUP_ROOT}/{dataset}"

    subprocess.check_output(command, shell=True)

    return jsonify(
        {
            "status": "started",
            "archive": archive_path,
            "target_bucket": BACKUP_BUCKET,
        }
    )