from database.database import Database
from models.repair import Repair


class RepairService:

    def __init__(self):
        self.db = Database()

    def get_all_repairs(self):
        rows = self.db.fetchall("""
            SELECT
                r.*,
                v.plate_number AS vehicle_plate,
                v.model AS vehicle_model,
                m.name AS mechanic_name
            FROM repairs r
            LEFT JOIN vehicles v ON v.id = r.vehicle_id
            LEFT JOIN mechanics m ON m.id = r.mechanic_id
            ORDER BY r.date DESC, r.id DESC
        """)

        return [Repair.from_row(row) for row in rows]

    def get_repairs_by_vehicle(self, vehicle_id):
        rows = self.db.fetchall("""
            SELECT
                r.*,
                v.plate_number AS vehicle_plate,
                v.model AS vehicle_model,
                m.name AS mechanic_name
            FROM repairs r
            LEFT JOIN vehicles v ON v.id = r.vehicle_id
            LEFT JOIN mechanics m ON m.id = r.mechanic_id
            WHERE r.vehicle_id = ?
            ORDER BY r.date DESC, r.id DESC
        """, (vehicle_id,))

        return [Repair.from_row(row) for row in rows]

    def get_repair_by_id(self, repair_id):
        row = self.db.fetchone("""
            SELECT
                r.*,
                v.plate_number AS vehicle_plate,
                v.model AS vehicle_model,
                m.name AS mechanic_name
            FROM repairs r
            LEFT JOIN vehicles v ON v.id = r.vehicle_id
            LEFT JOIN mechanics m ON m.id = r.mechanic_id
            WHERE r.id = ?
        """, (repair_id,))

        return Repair.from_row(row)

    def add_repair(self, repair: Repair):
        self.db.execute("""
            INSERT INTO repairs(
                vehicle_id,
                date,
                mileage,
                repair_type,
                reason,
                work_description,
                mechanic_id,
                status,
                cost,
                comment
            )
            VALUES(?,?,?,?,?,?,?,?,?,?)
        """, (
            repair.vehicle_id,
            repair.date,
            repair.mileage,
            repair.repair_type,
            repair.reason,
            repair.work_description,
            repair.mechanic_id,
            repair.status,
            repair.cost,
            repair.comment,
        ))

    def add_repair_with_parts(self, repair: Repair, parts):
        self.add_repair(repair)

        self.update_vehicle_mileage_from_repair(repair.vehicle_id, repair.mileage)

        row = self.db.fetchone("SELECT last_insert_rowid() AS id")
        repair.id = row["id"]

        for item in parts:
            self.add_repair_part(
                repair.id,
                item["part_id"],
                item["quantity"],
                item["price"],
                item.get("comment", ""),
            )

    def replace_repair_parts(self, repair_id, parts):
        issued_row = self.db.fetchone("""
            SELECT COALESCE(SUM(quantity), 0) AS quantity
            FROM transactions
            WHERE repair_id = ?
              AND operation = 'Выдача'
        """, (repair_id,))

        issued_quantity = int(issued_row["quantity"] or 0)
        if issued_quantity > 0:
            raise ValueError(
                "Нельзя изменить состав запчастей ремонта, "
                "по которому уже была выполнена выдача со склада."
            )

        self.db.execute(
            "DELETE FROM repair_parts WHERE repair_id=?",
            (repair_id,)
        )

        for item in parts:
            self.add_repair_part(
                repair_id,
                item["part_id"],
                item["quantity"],
                item["price"],
                item.get("comment", ""),
            )

    def update_repair(self, repair: Repair):
        self.db.execute("""
            UPDATE repairs
            SET
                vehicle_id=?,
                date=?,
                mileage=?,
                repair_type=?,
                reason=?,
                work_description=?,
                mechanic_id=?,
                status=?,
                cost=?,
                comment=?
            WHERE id=?
        """, (
            repair.vehicle_id,
            repair.date,
            repair.mileage,
            repair.repair_type,
            repair.reason,
            repair.work_description,
            repair.mechanic_id,
            repair.status,
            repair.cost,
            repair.comment,
            repair.id,
        ))

        self.update_vehicle_mileage_from_repair(
            repair.vehicle_id,
            repair.mileage,
        )

    def update_vehicle_mileage_from_repair(self, vehicle_id, mileage):
        if vehicle_id is None or mileage is None:
            return

        self.db.execute("""
            UPDATE vehicles
            SET mileage = ?
            WHERE id = ?
              AND COALESCE(mileage, 0) < ?
        """, (mileage, vehicle_id, mileage))

    def delete_repair(self, repair_id):
        issued_row = self.db.fetchone("""
            SELECT COALESCE(SUM(quantity), 0) AS quantity
            FROM transactions
            WHERE repair_id = ?
              AND operation = 'Выдача'
        """, (repair_id,))

        issued_quantity = int(issued_row["quantity"] or 0)
        if issued_quantity > 0:
            raise ValueError(
                "Нельзя удалить ремонт, по которому уже была выполнена "
                "выдача запчастей со склада."
            )

        self.db.execute(
            "DELETE FROM repair_parts WHERE repair_id=?",
            (repair_id,)
        )

        self.db.execute(
            "DELETE FROM repairs WHERE id=?",
            (repair_id,)
        )

    def get_repair_parts(self, repair_id):
        return self.db.fetchall("""
            SELECT
                rp.id,
                rp.repair_id,
                rp.part_id,
                rp.quantity,
                rp.price,
                rp.comment,
                p.article,
                p.name,
                p.unit,
                COALESCE((
                    SELECT SUM(t.quantity)
                    FROM transactions t
                    WHERE t.repair_id = rp.repair_id
                      AND t.part_id = rp.part_id
                      AND t.operation = 'Выдача'
                ), 0) AS issued_quantity
            FROM repair_parts rp
            JOIN parts p ON p.id = rp.part_id
            WHERE rp.repair_id = ?
            ORDER BY rp.id
        """, (repair_id,))

    def add_repair_part(self, repair_id, part_id, quantity, price, comment=""):
        self.db.execute("""
            INSERT INTO repair_parts(
                repair_id,
                part_id,
                quantity,
                price,
                comment
            )
            VALUES(?,?,?,?,?)
        """, (repair_id, part_id, quantity, price, comment))

    def delete_repair_part(self, repair_part_id):
        self.db.execute(
            "DELETE FROM repair_parts WHERE id=?",
            (repair_part_id,)
        )
