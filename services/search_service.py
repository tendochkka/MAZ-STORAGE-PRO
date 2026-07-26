from services.part_service import PartService


class SearchService:

    def __init__(self):

        self.part_service = PartService()

    def search_parts(self, text: str):

        text = text.lower().strip()

        parts = self.part_service.get_all_parts()

        if text == "":
            return parts

        result = []

        for part in parts:

            if (
                text in part.article.lower()
                or text in part.name.lower()
                or text in part.location_code.lower()
                or text in part.manufacturer.lower()
                or text in part.compatible_models.lower()
            ):
                result.append(part)

        return result