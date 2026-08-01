from database.database import Database
from models.vehicle import Vehicle


class VehicleService:

    def __init__(self):
        self.db = Database()

    def get_all_vehicles(self):
        rows = self.db.fetchall("""
            SELECT *
            FROM vehicles
            ORDER BY plate_number
        """)

        return [Vehicle.from_row(row) for row in rows]

    def get_vehicle_by_id(self, vehicle_id):
        row = self.db.fetchone("""
            SELECT *
            FROM vehicles
            WHERE id=?
        """, (vehicle_id,))

        return Vehicle.from_row(row)

    def add_vehicle(self, vehicle: Vehicle):
        self.db.execute("""
            INSERT INTO vehicles(
                plate_number,
                model,
                garage_number,
                vin,
                mileage,
                comment
            )
            VALUES(?,?,?,?,?,?)
        """, vehicle.to_tuple())

    def update_vehicle(self, vehicle: Vehicle):
        self.db.execute("""
            UPDATE vehicles
            SET
                plate_number=?,
                model=?,
                garage_number=?,
                vin=?,
                mileage=?,
                comment=?
            WHERE id=?
        """, (
            vehicle.plate_number,
            vehicle.model,
            vehicle.garage_number,
            vehicle.vin,
            vehicle.mileage,
            vehicle.comment,
            vehicle.id,
        ))

    def delete_vehicle(self, vehicle_id):
        self.db.execute(
            "DELETE FROM vehicles WHERE id=?",
            (vehicle_id,)
        )
