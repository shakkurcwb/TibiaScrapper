import re

from time import sleep

from src.tibia_bazaar.pages import Page, CurrentAuctionsPage, AuctionHistoryPage
# from src.tibia_bazaar.transformers import Transformer, CurrentAuctionsTransformer, AuctionHistoryTransformer
from src.tibia_bazaar.scrapper import TibiaBazaarScrapper
from src.tibia_bazaar.storages import Storage, CurrentAuctionsStorage, AuctionHistoryStorage


def scrap_current_auctions():
    page = CurrentAuctionsPage()
    storage = CurrentAuctionsStorage()

    TibiaBazaarScrapper(page, storage).auto_scrap()


def scrap_auction_history():
    page = AuctionHistoryPage()
    storage = AuctionHistoryStorage()

    TibiaBazaarScrapper(page, storage).auto_scrap()

if __name__ == '__main__':
    scrap_current_auctions()
    # scrap_auction_history()
