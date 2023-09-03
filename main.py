import time

from src.tibia_bazaar.tasks import (
    scrap_current_auctions,
    scrap_auction_details,
    filter_auctions,
    notify_auctions,
)


def auto_run():
    while True:
        try:
            run()
        except Exception as e:
            print(str(e))
            exit(1)

        print("Next execution in 5 minutes...")

        time.sleep(300)


def run():
    # scrap current auctions (10 pages is enough)
    scrap_current_auctions(1, 10)

    # scrap auction details for current auctions (not necessary)
    # scrap_auction_details()

    # filter auctions
    filter_auctions()

    # notify auctions
    notify_auctions()


if __name__ == "__main__":
    auto_run()
