import json
import azure.functions as func
from db import get_conn

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        body = req.get_json()
    except ValueError:
        return func.HttpResponse("invalid json", status_code=400)

    items = body.get("items", [])
    conn = get_conn()
    cur = conn.cursor()

    for item in items:
        sku = item["sku"]
        name = item["name"]
        price = int(item["price_cents"])
        qty = int(item["quantity"])

        cur.execute("SELECT id FROM products WHERE sku = ?", (sku,))
        row = cur.fetchone()
        if row:
            pid = row[0]
            cur.execute(
                "UPDATE products SET name = ?, price_cents = ? WHERE id = ?",
                (name, price, pid),
            )
        else:
            cur.execute(
                "INSERT INTO products (sku, name, price_cents) VALUES (?, ?, ?)",
                (sku, name, price),
            )
            cur.execute("SELECT SCOPE_IDENTITY()")
            pid = int(cur.fetchone()[0])

        cur.execute(
            "UPDATE inventory SET quantity = ? WHERE product_id = ?",
            (qty, pid),
        )
        if cur.rowcount == 0:
            cur.execute(
                "INSERT INTO inventory (product_id, quantity) VALUES (?, ?)",
                (pid, qty),
            )

    conn.commit()
    conn.close()
    return func.HttpResponse(
        json.dumps({"ok": True}),
        mimetype="application/json"
    )
