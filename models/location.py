from dataclasses import dataclass


@dataclass
class Location:
    """
    Модель места хранения.
    """

    id: int | None = None

    zone: str = ""
    rack: str = ""
    shelf: str = ""
    cell: str = ""

    description: str = ""

    @property
    def code(self) -> str:
        """
        Возвращает адрес хранения.

        Пример:
        A-01-03-05
        """

        return f"{self.zone}-{self.rack}-{self.shelf}-{self.cell}"

    def to_dict(self):

        return {
            "id": self.id,
            "zone": self.zone,
            "rack": self.rack,
            "shelf": self.shelf,
            "cell": self.cell,
            "description": self.description,
        }

    @classmethod
    def from_row(cls, row):

        if row is None:
            return None

        return cls(
            id=row["id"],
            zone=row["zone"],
            rack=row["rack"],
            shelf=row["shelf"],
            cell=row["cell"],
            description=row["description"] or "",
        )

    def __str__(self):

        return self.code