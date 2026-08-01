from dataclasses import dataclass


@dataclass
class Mechanic:
    id: int | None = None
    name: str = ""

    @classmethod
    def from_row(cls, row):
        if row is None:
            return None

        return cls(
            id=row["id"],
            name=row["name"] or "",
        )
