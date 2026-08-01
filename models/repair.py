from dataclasses import dataclass


@dataclass
class Repair:
    id: int | None = None
    vehicle_id: int | None = None
    date: str = ""
    mileage: int = 0
    repair_type: str = ""
    reason: str = ""
    work_description: str = ""
    mechanic_id: int | None = None
    status: str = "Выполнен"
    cost: float = 0.0
    comment: str = ""
    vehicle_plate: str = ""
    vehicle_model: str = ""
    mechanic_name: str = ""

    @classmethod
    def from_row(cls, row):
        if row is None:
            return None

        return cls(
            id=row["id"],
            vehicle_id=row["vehicle_id"],
            date=row["date"] or "",
            mileage=row["mileage"] or 0,
            repair_type=row["repair_type"] or "",
            reason=row["reason"] or "",
            work_description=row["work_description"] or "",
            mechanic_id=row["mechanic_id"],
            status=row["status"] or "",
            cost=row["cost"] or 0.0,
            comment=row["comment"] or "",
            vehicle_plate=row["vehicle_plate"] if "vehicle_plate" in row.keys() else "",
            vehicle_model=row["vehicle_model"] if "vehicle_model" in row.keys() else "",
            mechanic_name=row["mechanic_name"] if "mechanic_name" in row.keys() else "",
        )
