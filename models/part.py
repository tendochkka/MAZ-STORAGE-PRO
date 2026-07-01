from dataclasses import dataclass


@dataclass
class Part:
    id: int | None = None

    article: str = ""

    name: str = ""

    quantity: int = 0

    location: str = ""

    location_id: int | None = None

    min_quantity: int = 0

    price: float = 0.0

    manufacturer: str = ""

    compatible_models: str = ""

    unit: str = ""

    comment: str = ""