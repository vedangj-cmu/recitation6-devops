import os
import json
import requests
import azure.functions as func
from db import get_conn

WAREHOUSE_URL = os.environ.get("APPSETTING_WAREHOUSE_URL")  # e.g. APIM /warehouse URL

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        body = req.get_json()
    except ValueError:
        return func.HttpResponse("invalid json", status_code=400)

    email = body.get("email")
    items = body.get("items", [])
    if not email or not items:
        return func.HttpResponse("email and items required", status_code=400)

    conn = get_conn()
    cur = conn.cursor()

    order_lines = []
    for item in items:
        sku = item["sku"]
        qty = int(item["quantity"])
        cur.execute("""
            SELECT i.quantity, p.id, p.price_cents
            FROM inventory i
            JOIN products p ON i.product_id = p.id
            WHERE p.sku = ?
        """, (sku,))
        row = cur.fetchone()
        if not row or row[0] < qty:
            conn.close()
            return func.HttpResponse(
                f"insufficient inventory for {sku}",
                status_code=400
            )
        order_lines.append({
            "sku": sku,
            "product_id": row[1],
            "quantity": qty,
            "unit_price_cents": row[2],
        })

    payment_success = True
    if not payment_success:
        conn.close()
        return func.HttpResponse("payment failed", status_code=402)

    cur.execute(
    "INSERT INTO orders (customer_email, status) OUTPUT INSERTED.id VALUES (?, ?)",
    (email, "PAID"),
)
    order_id = cur.fetchone()[0]

    for line in order_lines:
        cur.execute(
            """
            INSERT INTO order_items (order_id, product_id, quantity, unit_price_cents)
            VALUES (?, ?, ?, ?)
            """,
            (
                order_id,
                line["product_id"],
                line["quantity"],
                line["unit_price_cents"],
            ),
        )
        cur.execute(
            "UPDATE inventory SET quantity = quantity - ? WHERE product_id = ?",
            (line["quantity"], line["product_id"]),
        )

    conn.commit()
    conn.close()

    payload = {
        "order_id": order_id,
        "email": email,
        "items": order_lines,
    }

    if WAREHOUSE_URL:
        try:
            requests.post(WAREHOUSE_URL, json=payload, timeout=2)
        except Exception:
            pass

    return func.HttpResponse(
        json.dumps({"ok": True, "order_id": order_id}),
        mimetype="application/json"
    )
