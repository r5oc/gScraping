from gScraping import Scraping
from os import path

if __name__ == "__main__":
    print(f"Executing {path.basename(__file__)}")
    scraping = Scraping()
    scraping.request()
    scraping.save_requests()