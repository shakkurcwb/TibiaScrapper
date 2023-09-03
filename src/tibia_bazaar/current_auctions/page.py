from src.helpers import Page


class CurrentAuctionsPage(Page):
    BASE_URL = (
        "https://www.tibia.com/charactertrade/?subtopic=currentcharactertrades&{}"
    )

    PARAMS = {
        "profession": None,
        "levelrangefrom": None,
        "levelrangeto": None,
        "world": None,
        "worldpvptype": None,
        "worldbattleyestate": None,
        "skillid": None,
        "skillrangefrom": None,
        "skillrangeto": None,
        "order_column": None,
        "order_direction": None,
        "searchtype": None,
        "currentpage": None,
    }

    HTML_FOLDER = "storage/tibia_bazaar/current_auctions/html"
    JSON_FOLDER = "storage/tibia_bazaar/current_auctions/json"

    def __init__(self):
        super().__init__(self.BASE_URL, self.PARAMS)
