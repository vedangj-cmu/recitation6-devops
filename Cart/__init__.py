import json
import azure.functions as func
from db import get_conn

def main(req: func.HttpRequest) -> func.HttpResponse:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT p.sku, p.name, p.price_cents, i.quantity
        FROM products p
        JOIN inventory i ON p.id = i.product_id
        WHERE i.quantity > 0
    """)
    rows = cur.fetchall()
    conn.close()

    items = [
        {
            "sku": r[0],
            "name": r[1],
            "price_cents": r[2],
            "quantity": r[3],
        }
        for r in rows
    ]

    return func.HttpResponse(
        json.dumps({"items": items}),
        mimetype="application/json"
    )
