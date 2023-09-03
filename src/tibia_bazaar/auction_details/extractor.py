from datetime import datetime

from bs4 import BeautifulSoup


class AuctionDetailsExtractor(object):
    DATE_FORMAT = "%b %d %Y, %H:%M %z"
    DATE_FORMAT_ALT = "%b %d %Y, %H:%M:%S %z"

    def __init__(self, html):
        self.html = html

    def extract(self):
        soup = BeautifulSoup(self.html, "html.parser")

        div_tag = soup.find("div", class_="Auction")
        character_name = div_tag.find("div", class_="AuctionCharacterName").text

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
        auction_end_date = str(datetime.strptime(auction_end_string, self.DATE_FORMAT))

        bid_label_tag = div_tag.find(text=["Minimum Bid:", "Current Bid:"])
        bid_value = bid_label_tag.find_next(class_="ShortAuctionDataValue").b.get_text(
            strip=True
        )
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

            main_items.append({"image_url": item_url, "description": item_description})

        details, skills = {}, {}
        details_tag = soup.find("table", {"id": "CharacterDetails"})
        for tr_tag in details_tag.find_all("tr"):
            numeric_details = [
                "experience",
                "gold",
                "capacity",
                "mana",
                "hit_points",
                "spent_charm_points",
                "hunting_task_points",
            ]

            label_tags = tr_tag.find_all("span", class_="LabelV")
            for label_tag in label_tags:
                title = (
                    label_tag.text.replace(":", "").strip().lower().replace(" ", "_")
                )
                value = label_tag.next_sibling.text.strip()

                if title == "creation_date":
                    value_string = value.replace("CEST", "+0200").replace(
                        "CET", "+0200"
                    )
                    value = str(datetime.strptime(value_string, self.DATE_FORMAT_ALT))

                if title in numeric_details:
                    value = int(value.replace(",", ""))

                if isinstance(value, str) and value.isnumeric():
                    value = int(value)

                details[title] = value

            label_alt_tags = tr_tag.find_all("td", class_="LabelColumn")
            for label_alt_tag in label_alt_tags:
                skill = label_alt_tag.text.strip().lower().replace(" ", "_")
                amount = label_alt_tag.next_sibling.text
                skills[skill] = int(amount)

        all_items = []
        items_tag = soup.find("div", {"id": "ItemSummary"})
        icon_tags = items_tag.find_all("div", class_="CVIconObject")
        for icon_tag in icon_tags:
            img_tag = icon_tag.find("img")
            item_description = icon_tag["title"]
            item_url = img_tag["src"]

            all_items.append({"image_url": item_url, "description": item_description})

        store_items = []
        store_items_tag = soup.find("div", {"id": "StoreItemSummary"})
        icon_tags = store_items_tag.find_all("div", class_="CVIconObject")
        for icon_tag in icon_tags:
            img_tag = icon_tag.find("img")
            item_description = icon_tag["title"]
            item_url = img_tag["src"]

            store_items.append({"image_url": item_url, "description": item_description})

        mounts = []
        mounts_tag = soup.find("div", {"id": "Mounts"})
        icon_tags = mounts_tag.find_all("div", class_="CVIcon")
        for icon_tag in icon_tags:
            mount_description = icon_tag["title"]
            mount_url = img_tag["src"]

            mounts.append({"image_url": mount_url, "description": mount_description})

        store_mounts = []
        store_mounts_tag = soup.find("div", {"id": "StoreMounts"})
        icon_tags = store_mounts_tag.find_all("div", class_="CVIcon")
        for icon_tag in icon_tags:
            mount_description = icon_tag["title"]
            mount_url = img_tag["src"]

            store_mounts.append(
                {"image_url": mount_url, "description": mount_description}
            )

        outfits = []
        outifts_tag = soup.find("div", {"id": "Outfits"})
        icon_tags = outifts_tag.find_all("div", class_="CVIcon")
        for icon_tag in icon_tags:
            outfit_tag = icon_tag.find("img")

            outfit_description = icon_tag["title"]
            outfit_url = outfit_tag["src"]

            outfits.append({"image_url": outfit_url, "description": outfit_description})

        store_outfits = []
        store_outifts_tag = soup.find("div", {"id": "StoreOutfits"})
        icon_tags = store_outifts_tag.find_all("div", class_="CVIcon")
        for icon_tag in icon_tags:
            outfit_tag = icon_tag.find("img")

            outfit_description = icon_tag["title"]
            outfit_url = outfit_tag["src"]

            store_outfits.append(
                {"image_url": outfit_url, "description": outfit_description}
            )

        familiars = []
        familiars_tag = soup.find("div", {"id": "Familiars"})
        icon_tags = familiars_tag.find_all("div", class_="CVIcon")
        for icon_tag in icon_tags:
            familiar_description = icon_tag["title"]
            familiar_url = img_tag["src"]

            familiars.append(
                {"image_url": familiar_url, "description": familiar_description}
            )

        return {
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
            **details,
            "skills": skills,
            "main_features": features,
            "main_items": main_items,
            "all_items": all_items,
            "store_items": store_items,
            "mounts": mounts,
            "store_mounts": store_mounts,
            "outfits": outfits,
            "store_outfits": store_outfits,
        }
