import requests


class Page(object):
    def __init__(self, url, params = None):
        self.url = url
        self.params = params or {}

    def set_params(self, params):
        self.params.update(params)

    def get_param(self, key, default = None):
        return self.params.get(key, default)

    def get_url(self):
        params = []
        for key, value in self.params.items():
            if value:
                params.append(f"{key}={value}")

        return self.url.format("&".join(params))

    def fetch_content(self):
        url = self.get_url()
        try:
            response = requests.get(url)

            if response.status_code == 200:
                return response.text
            else:
                raise Exception(f"Error requesting page: {url} - ({response.status_code}) {response.text}")

        except Exception as e:
            raise Exception(f"Error requesting page: {url} - {e}")


class CurrentAuctionsPage(Page):
    BASE_URL = "https://www.tibia.com/charactertrade/?subtopic=currentcharactertrades&{}"

    FILTERS = {
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

    def __init__(self):
        super().__init__(self.BASE_URL, self.FILTERS)


class AuctionHistoryPage(Page):
    BASE_URL = "https://www.tibia.com/charactertrade/?subtopic=pastcharactertrades&{}"

    FILTERS = {
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
        "currentpage": None,
    }

    def __init__(self):
        super().__init__(self.BASE_URL, self.FILTERS)
