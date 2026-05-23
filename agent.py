

import re, os
from db import get_conn

def interpret(text):
    text = text.lower()

    # Example: restore database testdb from c:\file.bak
    m = re.search(r"restore database (.+?) from (.+)", text)
    if m:
        return {"action": "restore", "db": m.group(1), "file": m.group(2)}

    # Example: restore latest to testdb
    m = re.search(r"restore latest to (.+)", text)
    if m:
        files = sorted(os.listdir(os.getenv("BACKUP_DIR")), reverse=True)
        bak = [f for f in files if f.endswith(".bak")][0]
        return {
            "action": "restore",
            "db": m.group(1),
            "file": os.path.join(os.getenv("BACKUP_DIR"), bak)
        }

    return {"action": "unknown"}


def restore(db, file):
    conn = get_conn()
    cursor = conn.cursor()

    sql = f"""
    RESTORE DATABASE [{db}]
    FROM DISK='{file}'
    WITH REPLACE
    """

    cursor.execute(sql)
    conn.commit()

    return f"Restored {db}"


def run_agent(command):
    parsed = interpret(command)

    if parsed["action"] == "restore":
        return restore(parsed["db"], parsed["file"])

    return "Command not understood"
