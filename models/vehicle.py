from dataclasses import dataclass


@dataclass
class Vehicle:
    id: int | None = None
    plate_number: str = ""
    model: str = ""
    garage_number: str = ""
    vin: str = ""
    mileage: int = 0
    comment: str = ""

    @classmethod
    def from_row(cls, row):
        if row is None:
            return None

        return cls(
            id=row["id"],
            plate_number=row["plate_number"] or "",
            model=row["model"] or "",
            garage_number=row["garage_number"] or "",
            vin=row["vin"] if "vin" in row.keys() and row["vin"] else "",
            mileage=row["mileage"] or 0,
            comment=row["comment"] or "",
        )

    def to_tuple(self):
        return (
            self.plate_number,
            self.model,
            self.garage_number,
            self.vin,
            self.mileage,
            self.comment,
        )
