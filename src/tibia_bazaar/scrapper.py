import re

from time import sleep


class TibiaBazaarScrapper(object):
    SLEEP_SECONDS = 6
    SLEEP_PAGES_INTERVAL = 20

    def __init__(self, page, storage):
        self.page = page
        self.storage = storage

    def _calculate_workload(self):
        per_page = 0
        total_records = 0    
        number_of_pages = 0

        # fetch page content
        html = self.page.fetch_content()

        # get number of auctions per page
        per_page = len(re.findall(re.escape('<div class="Auction">'), html))

        # get total number of auctions
        match = re.search(r'Results:\s*([\d,]+)', html)

        if not match:
            raise Exception("Error: total number of auctions not found")

        total_records = int(match.group(1).replace(',', ''))

        # get number of pages
        number_of_pages = total_records // per_page

        if total_records % per_page > 0:
            number_of_pages += 1

        return per_page, total_records, number_of_pages

    def auto_scrap(self, start_page = 1, max_pages = None):
        print(f"Starting...")

        print(f"Page Url: {self.page.url}")
        print(f"Storage Path: {self.storage.path}")

        per_page, total_records, number_of_pages = self._calculate_workload()

        print(f"Current page: {start_page}")
        print(f"Total records: {total_records}")
        print(f"Records per page: {per_page}")
        print(f"Number of pages: {number_of_pages}")

        for i in range(start_page, number_of_pages + 1):
            # stop if max pages is reached
            if max_pages and i > max_pages:
                print(f"Max pages reached ({max_pages})")
                break

            # sleep for X seconds every Y pages
            if i % self.SLEEP_PAGES_INTERVAL == 0:
                print(f"Sleeping for {self.SLEEP_SECONDS} seconds")
                sleep(self.SLEEP_SECONDS)

            # set page number
            self.page.set_params({
                "currentpage": i,
            })

            # fetch page content
            html = self.page.fetch_content()

            # get file path
            file_path = self.storage.get_path(f"page_{i}.html")

            # save file
            with open(file_path, "w") as f:
                f.write(html)

            print(f"- Page {i}/{number_of_pages} saved")

        print("Done.")
