from dataclasses import dataclass


@dataclass
class Part:
    id: int | None = None

    article: str = ""
    name: str = ""

    quantity: int = 0
    location_id: int | None = None

    min_quantity: int = 0

    price: float = 0.0

    manufacturer: str = ""

    compatible_models: str = ""

    unit: str = ""

    comment: str = ""

    location_code: str = ""

    @classmethod
    def from_row(cls, row):

        if row is None:
            return None

        return cls(
            id=row["id"],
            article=row["article"],
            name=row["name"],
            quantity=row["quantity"],
            location_id=row["location_id"],
            min_quantity=row["min_quantity"],
            price=row["price"],
            manufacturer=row["manufacturer"] or "",
            compatible_models=row["compatible_models"] or "",
            unit=row["unit"] or "",
            comment=row["comment"] or "",
            location_code=row["location_code"] if "location_code" in row.keys() else "",
        )

    def to_tuple(self):

        return (
            self.article,
            self.name,
            self.quantity,
            self.location_id,
            self.min_quantity,
            self.price,
            self.manufacturer,
            self.compatible_models,
            self.unit,
            self.comment,
        )

    def __str__(self):

        return f"{self.article} — {self.name}"