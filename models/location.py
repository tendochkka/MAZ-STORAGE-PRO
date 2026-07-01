from dataclasses import dataclass


@dataclass
class Location:

    id: int | None = None

    zone: str = ""

    rack: str = ""

    shelf: str = ""

    cell: str = ""

    description: str = ""

    @property
    def code(self):

        return f"{self.zone}-{self.rack}-{self.shelf}-{self.cell}"