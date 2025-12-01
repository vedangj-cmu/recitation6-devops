import json
import azure.functions as func
from db import get_conn

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        body = req.get_json()
    except ValueError:
        return func.HttpResponse("invalid json", status_code=400)

    order_id = body.get("order_id")
    if not order_id:
        return func.HttpResponse("order_id required", status_code=400)

    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "UPDATE orders SET status = ? WHERE id = ?",
        ("PACKING", int(order_id)),
    )
    conn.commit()
    conn.close()

    return func.HttpResponse(
        json.dumps({"ok": True}),
        mimetype="application/json"
    )
