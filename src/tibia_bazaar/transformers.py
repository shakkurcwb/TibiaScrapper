class Transformer(object):
    def transform(self):
        raise NotImplementedError()


class CurrentAuctionsTransformer(Transformer):
    def transform(self, soup):
        auctions = []

        table = soup.find("table", {"class": "Table3"})
        rows = table.find_all("tr")

        for row in rows[1:]:
            columns = row.find_all("td")

            auction = {
                "name": columns[0].text.strip(),
                "level": columns[1].text.strip(),
                "vocation": columns[2].text.strip(),
                "world": columns[3].text.strip(),
                "price": columns[4].text.strip(),
                "bid": columns[5].text.strip(),
                "ends": columns[6].text.strip(),
                "status": columns[7].text.strip(),
            }

            auctions.append(auction)

        return auctions
