from src.helpers import Page


class AuctionDetailsPage(Page):
    BASE_URL = "https://www.tibia.com/charactertrade/?subtopic=currentcharactertrades&page=details&{}"

    PARAMS = {
        "auctionid": None,
    }

    HTML_FOLDER = "storage/tibia_bazaar/auction_details/html"
    JSON_FOLDER = "storage/tibia_bazaar/auction_details/json"

    def __init__(self):
        super().__init__(self.BASE_URL, self.PARAMS)
