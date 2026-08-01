from datetime import datetime

from database.database import Database


class TransactionService:

    def __init__(self):
        self.db = Database()

    def get_issued_quantity(self, repair_id, part_id):
        row = self.db.fetchone("""
            SELECT COALESCE(SUM(quantity), 0) AS quantity
            FROM transactions
            WHERE repair_id = ?
              AND part_id = ?
              AND operation = 'Выдача'
        """, (repair_id, part_id))
        return int(row["quantity"] or 0)

    def issue_repair_parts(self, repair_id, vehicle_id, mechanic_id, parts):
        # Сначала проверяем наличие всех недостающих количеств,
        # чтобы не начать выдачу при недостаточном остатке одной из позиций.
        to_issue = []

        for item in parts:
            required = int(item["quantity"] or 0)
            issued = self.get_issued_quantity(repair_id, item["part_id"])
            remaining = required - issued

            if remaining <= 0:
                continue

            row = self.db.fetchone("SELECT id, name, quantity, price FROM parts WHERE id=?", (item["part_id"],))
            if row is None:
                raise ValueError(f"Запчасть ID {item['part_id']} не найдена")

            stock = int(row["quantity"] or 0)
            if stock < remaining:
                raise ValueError(
                    f"Недостаточно запчасти «{row['name']}»: "
                    f"нужно {remaining}, в наличии {stock}"
                )

            to_issue.append({
                "part_id": item["part_id"],
                "quantity": remaining,
                "price": float(item.get("price") or row["price"] or 0),
                "comment": item.get("comment", ""),
            })

        if not to_issue:
            return 0

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for item in to_issue:
            self.db.execute("""
                UPDATE parts
                SET quantity = quantity - ?
                WHERE id = ?
            """, (item["quantity"], item["part_id"]))

            self.db.execute("""
                INSERT INTO transactions(
                    date, operation, part_id, quantity, vehicle_id,
                    mechanic_id, user_id, repair_id, comment
                )
                VALUES(?,?,?,?,?,?,?,?,?)
            """, (
                now,
                "Выдача",
                item["part_id"],
                item["quantity"],
                vehicle_id,
                mechanic_id,
                None,
                repair_id,
                item["comment"],
            ))

        return sum(item["quantity"] for item in to_issue)
