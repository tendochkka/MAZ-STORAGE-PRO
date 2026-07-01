from dataclasses import dataclass


@dataclass
class Vehicle:

    id: int | None = None

    plate_number: str = ""

    model: str = ""

    garage_number: str = ""

    mileage: int = 0

    comment: str = ""