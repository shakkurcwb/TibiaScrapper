import re
import arrow

from datetime import datetime

from bs4 import BeautifulSoup


class CurrentAuctionsExtractor(object):
    DATE_FORMAT = "%b %d %Y, %H:%M %z"

    def __init__(self, html):
        self.html = html

    def extract(self):
        soup = BeautifulSoup(self.html, "html.parser")

        auctions = []

        auctions_tag = soup.find_all("div", {"class": "Auction"})
        for div_tag in auctions_tag:
            name_a_tag = div_tag.find("div", class_="AuctionCharacterName").a
            character_name = name_a_tag.text
            auction_url = name_a_tag["href"]
            auction_id = int(re.search(r"auctionid=(\d+)", auction_url).group(1))

            header_tag = div_tag.find("div", class_="AuctionHeader").get_text()
            info_parts = header_tag.split("|")
            character_level = int(info_parts[0].split(":")[1].strip())
            character_vocation = info_parts[1].split(":")[1].strip()
            character_gender = info_parts[2].strip()

            world_tag = div_tag.find("div", class_="AuctionHeader").find(
                "a", target="_blank"
            )
            world_name = world_tag.text
            world_url = world_tag["href"]

            img_tag = div_tag.find("img", class_="AuctionOutfitImage")
            character_image_url = img_tag["src"]

            auction_start_label_tag = div_tag.find(text="Auction Start:")
            auction_start_value = auction_start_label_tag.find_next(
                class_="ShortAuctionDataValue"
            ).get_text(strip=True)
            auction_start_string = auction_start_value.replace("CEST", "+0200").replace(
                "CET", "+0200"
            )
            auction_start_date = str(
                datetime.strptime(auction_start_string, self.DATE_FORMAT)
            )

            auction_end_label_tag = div_tag.find(text="Auction End:")
            auction_end_value = auction_end_label_tag.find_next(
                class_="ShortAuctionDataValue"
            ).get_text(strip=True)
            auction_end_string = auction_end_value.replace("CEST", "+0200").replace(
                "CET", "+0200"
            )
            auction_end_date = str(
                datetime.strptime(auction_end_string, self.DATE_FORMAT)
            )

            bid_label_tag = div_tag.find(text=["Minimum Bid:", "Current Bid:"])
            bid_value = bid_label_tag.find_next(
                class_="ShortAuctionDataValue"
            ).b.get_text(strip=True)
            bid_value = float(bid_value.replace(",", ""))

            features = []
            entries_tags = div_tag.find_all("div", class_="Entry")
            for entry_tag in entries_tags:
                img_tag = entry_tag.find("img", class_="CharacterFeatureCategory")
                feature_url = img_tag["src"]
                feature_description = entry_tag.get_text(strip=True)

                features.append(
                    {"image_url": feature_url, "description": feature_description}
                )

            main_items = []
            icon_tags = div_tag.find_all("div", class_="CVIconObject")
            for icon_tag in icon_tags:
                img_tag = icon_tag.find("img")

                if icon_tag["title"] == "(no item for display selected)":
                    continue

                item_description = icon_tag["title"]
                item_url = img_tag["src"]

                main_items.append(
                    {"image_url": item_url, "description": item_description}
                )

            auctions.append(
                {
                    "auction_id": auction_id,
                    "auction_url": auction_url,
                    "character_image_url": character_image_url,
                    "character_name": character_name,
                    "character_level": character_level,
                    "character_vocation": character_vocation,
                    "character_gender": character_gender,
                    "world_name": world_name,
                    "world_url": world_url,
                    "auction_start_date": auction_start_date,
                    "auction_end_date": auction_end_date,
                    "bid": bid_value,
                    "main_features": features,
                    "main_items": main_items,
                }
            )

        return auctions
