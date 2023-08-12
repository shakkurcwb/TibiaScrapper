import os.path


class Storage(object):
    def __init__(self, folder):
        self.path = folder.strip("/")

    def get_path(self, filename):
        return os.path.join(self.path, filename)

    def get_file(self, filename):
        path = self.get_path(filename)

        if not os.path.isfile(path):
            raise Exception(f"File {path} not found")

        return path


class CurrentAuctionsStorage(Storage):
    def __init__(self):
        super().__init__("storage/tibia_bazaar/current_auctions/html")


class AuctionHistoryStorage(Storage):
    def __init__(self):
        super().__init__("storage/tibia_bazaar/auction_history/html")
