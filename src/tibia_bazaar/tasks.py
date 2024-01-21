import arrow
import telegram

from environs import Env

from time import sleep

from requests import HTTPError

from src.helpers import Request, HtmlFile, JsonFile, Timer, Folder

from src.tibia_bazaar.current_auctions.page import CurrentAuctionsPage
from src.tibia_bazaar.current_auctions.extractor import CurrentAuctionsExtractor

from src.tibia_bazaar.auction_details.page import AuctionDetailsPage
from src.tibia_bazaar.auction_details.extractor import AuctionDetailsExtractor


env = Env()
env.read_env()

TELEGRAM_BOT_TOKEN = env("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = env("TELEGRAM_CHAT_ID")


def clear_current_auctions_pages():
    print("Clearing current auctions pages")

    Folder(CurrentAuctionsPage.HTML_FOLDER).clear()
    Folder(CurrentAuctionsPage.JSON_FOLDER).clear()

    print("Cleared current auctions pages")

    return 1


def clear_auction_details_pages():
    print("Clearing auction details pages")

    Folder(AuctionDetailsPage.HTML_FOLDER).clear()
    Folder(AuctionDetailsPage.JSON_FOLDER).clear()

    print("Cleared auction details pages")

    return 1


def collect_current_auctions_pages(start=0, end=100):
    print("Collecting current auctions pages")

    page = CurrentAuctionsPage()

    timer = Timer()
    timer.start()

    print(f"Collecting pages from {start} to {end}")
    for i in range(start, end + 1):
        page.set_params(
            {
                "currentpage": i,
            }
        )

        try:
            html = Request(page).get()
        except HTTPError as e:
            print(f"- Page {i} failed - retrying...")
            sleep(6)

            try:
                html = Request(page).get()
            except Exception as e:
                print(f"- Page {i} failed - skipping...")
                continue

        HtmlFile(CurrentAuctionsPage.HTML_FOLDER, f"page_{i}.html").write(html)

        print(f"+ Page {i} collected")

    timer.end()
    minutes, seconds = timer.diff()

    print(
        f"Collected pages from {start} to {end} in {minutes} minutes and {seconds} seconds"
    )

    return 1


def extract_current_auctions_pages(start=0, end=100):
    print("Extracting current auctions pages")

    timer = Timer()
    timer.start()

    print(f"Extracting pages from {start} to {end}")
    for i in range(start, end + 1):
        html = HtmlFile(CurrentAuctionsPage.HTML_FOLDER, f"page_{i}.html").read()

        extractor = CurrentAuctionsExtractor(html)

        json = extractor.extract()

        JsonFile(CurrentAuctionsPage.JSON_FOLDER, f"page_{i}.json").write(json)

        print(f"+ Page {i} extracted")

    timer.end()
    minutes, seconds = timer.diff()

    print(
        f"Extracted pages from {start} to {end} in {minutes} minutes and {seconds} seconds"
    )

    return 1


def process_current_auctions_pages(start=0, end=100):
    print("Processing current auctions pages")

    timer = Timer()
    timer.start()

    auctions = {}

    print(f"Processing pages from {start} to {end}")
    for i in range(start, end + 1):
        json = JsonFile(CurrentAuctionsPage.JSON_FOLDER, f"page_{i}.json").read()

        for auction in json:
            # avoid duplicates
            if auction.get("auction_id") in auctions:
                continue

            auctions[auction.get("auction_id")] = auction

        print(f"+ Page {i} processed")

    timer.end()
    minutes, seconds = timer.diff()

    # sort by auction end date
    sorted_auctions = sorted(auctions.values(), key=lambda k: k["auction_end_date"])

    JsonFile("output/tibia_bazaar", "current_auctions.json").write(sorted_auctions)

    print(
        f"Processed pages from {start} to {end} in {minutes} minutes and {seconds} seconds"
    )

    return 1


def collect_auction_details_page(auction_id):
    print(f"Collecting auction details page for auction {auction_id}")

    page = AuctionDetailsPage()

    page.set_params(
        {
            "auctionid": auction_id,
        }
    )

    html = Request(page).get()

    HtmlFile(AuctionDetailsPage.HTML_FOLDER, f"auction_{auction_id}.html").write(html)

    print(f"+ Auction details page for auction {auction_id} collected")

    return 1


def extract_auction_details_page(auction_id):
    print(f"Extracting auction details page for auction {auction_id}")

    html = HtmlFile(AuctionDetailsPage.HTML_FOLDER, f"auction_{auction_id}.html").read()

    extractor = AuctionDetailsExtractor(html)

    json = extractor.extract()

    JsonFile(AuctionDetailsPage.JSON_FOLDER, f"auction_{auction_id}.json").write(json)

    print(f"+ Auction details page for auction {auction_id} extracted")

    return 1


def process_auction_details_page(auction_id):
    print(f"Processing auction details page for auction {auction_id}")

    inflated_auction = JsonFile(
        AuctionDetailsPage.JSON_FOLDER, f"auction_{auction_id}.json"
    ).read()

    auctions = JsonFile("output/tibia_bazaar", "current_auctions.json").read()

    for auction in auctions:
        # @todo: confirm it is integer
        if auction.get("auction_id") == auction_id:
            auction.update(inflated_auction)

    JsonFile("output/tibia_bazaar", "current_auctions.json").write(auctions)

    print(f"+ Auction details page for auction {auction_id} processed")

    return 1


def scrap_current_auctions(start=0, end=100):
    print("Scraping current auctions")

    timer = Timer()
    timer.start()

    clear_current_auctions_pages()

    collect_current_auctions_pages(start, end)
    extract_current_auctions_pages(start, end)
    process_current_auctions_pages(start, end)

    timer.end()
    minutes, seconds = timer.diff()

    print(
        f"Scrapping pages from {start} to {end} in {minutes} minutes and {seconds} seconds"
    )

    return 1


def scrap_auction_details_chunks(start=0, end=100):
    print(f"Scraping auction details for current auctions ({start} to {end})")

    timer = Timer()
    timer.start()

    auctions = JsonFile("output/tibia_bazaar", "current_auctions.json").read()

    print(f"Found {len(auctions)} auctions")

    i = 0
    for auction in auctions[start:end]:
        print(f"Scraping auction {auction.get('auction_id')}")
        auction_id = auction.get("auction_id")

        collect_auction_details_page(auction_id)
        extract_auction_details_page(auction_id)
        process_auction_details_page(auction_id)

        print(f"+ Auction {auction_id} scraped")

    timer.end()
    minutes, seconds = timer.diff()

    print(
        f"Scrapping pages from {start} to {end} in {minutes} minutes and {seconds} seconds"
    )

    return 1


def scrap_auction_details():
    auctions = JsonFile("output/tibia_bazaar", "current_auctions.json").read()

    chunks = [auctions[x : x + 100] for x in range(0, len(auctions), 100)]

    print(f"Got {len(auctions)} auctions in {len(chunks)} chunks")

    clear_auction_details_pages()

    for i, _ in enumerate(chunks):
        start = i * 100
        end = start + 100

        print(f"Starting chunk {i} ({start} to {end}")
        scrap_auction_details_chunks(start, end)

    return 1


def filter_auctions():
    """
    Filter auctions by:
    - character level (500+)
    - auction end date (less than 1 hour)
    - bid (less than 10k)

    These are my filters, you can change them as you wish.
    You may find this resource helpful as well: https://www.tibiaplus.com
    Good luck with your auctions! :)
    """
    print("Filtering auctions")

    auctions = JsonFile("output/tibia_bazaar", "current_auctions.json").read()

    now = arrow.get().to("America/Toronto")

    filtered_auctions = []
    for auction in auctions:
        # avoid characters below level 500
        if auction.get("character_level") < 500:
            continue

        end_date = arrow.get(auction.get("auction_end_date")).to("America/Toronto")

        # avoid auctions that already ended
        if end_date < now:
            continue

        # avoid auctions that end in more than 1 hour
        if end_date > now.shift(hours=+1):
            continue

        # avoid bids above 10k
        if auction.get("bid") > 10000:
            continue

        filtered_auctions.append(auction)

    # sort by auction end date
    sorted_auctions = sorted(filtered_auctions, key=lambda k: k["auction_end_date"])

    print(f"Filtered {len(auctions)} auctions to {len(filtered_auctions)} auctions")

    JsonFile("output/tibia_bazaar", "current_auctions_filtered.json").write(
        sorted_auctions
    )

    return 1


def notify_auctions():
    if not TELEGRAM_BOT_TOKEN:
        return

    print("Notifying auctions")

    auctions = JsonFile("output/tibia_bazaar", "current_auctions_filtered.json").read()

    if not auctions:
        print("No auctions to notify")
        bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            parse_mode=telegram.ParseMode.MARKDOWN,
            text="No auctions to notify",
        )
        return

    bot = telegram.Bot(TELEGRAM_BOT_TOKEN)

    text = [f"Upcoming Deals ({len(auctions)}):  \U0001F525"]
    for auction in auctions:
        auction_end_date_humanified = arrow.get(
            auction.get("auction_end_date")
        ).humanize()
        text.append(f"- [{auction.get('character_name')}]({auction.get('auction_url')}) ({auction.get('world_name')}) {auction.get('character_vocation')} {auction.get('character_level')} - ${auction.get('bid')} {auction_end_date_humanified}")

    # every 20 auctions, send a message
    for i in range(0, len(text), 20):
        bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            parse_mode=telegram.ParseMode.MARKDOWN,
            text="\n".join(text[i : i + 20]),
        )

    print("Notification sent to subscribers")

    return 1
