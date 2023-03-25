from gScraping.settings import Settings

import requests
from bs4 import BeautifulSoup
from os import path, makedirs
from datetime import datetime
from pandas import DataFrame


class Scraping(Settings):
    def __init__(self, url="", headers="", path_="./settings.json"):
        Settings.__init__(self, path_dictionary=path_)
        """Constructor"""

        if url != "":
            self.url = url
        else:
            if self.dictionary["url"] != "":
                self.url = self.dictionary["url"]
            else:
                print("Invalid url")
                exit()

        if headers != "":
            self.headers = headers
        else:
            if self.dictionary["headers"] != "":
                self.headers = self.dictionary["headers"]
            else:
                print("Invalid headers")
                exit()

        self.headers = {"User-Agent": self.dictionary["headers"]}


    def request(self):
        count = self.dictionary["next-page"]["start"]

        while True:
            
            try:
                url = self.url.replace("~~~", str(count))
            except AttributeError as e:
                print("\n[Invalid url]")
                exit()

            site = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(site.content, 'html.parser')
            products = soup.find_all(self.dictionary["card"]["tag"], self.dictionary["card"]["class"])

            if len(products) == 0:
                break

            print("Scraping page:", count)

            for product in products:
                for item, value in self.dictionary["products"].items():
                    try:
                        product_info = product.find(value["tag"], value["class"]).get_text()
                    except AttributeError:
                        product_info = ""
                    finally:
                        self.products_dictionary[item].append(product_info)

            count += self.dictionary["next-page"]["increment"]


    def save_requests(self, directory="./DataFrames"):

        try:
            makedirs(directory)
        except FileExistsError:
            pass

        dt = datetime.now()
        creation_date = dt.strftime("%d %b %Y %H %M %S %f")
        absolute_path = f"{directory}/data-frame {creation_date}.csv"

        if not path.isfile(absolute_path):
            count = 0
            for item, value in self.products_dictionary.items():
                if len(value) > 0:
                    count += 1

            if count != 0:
                data_frame = DataFrame(self.products_dictionary)
                data_frame.to_csv(f"{absolute_path}", encoding="utf-8", sep=";")
                print(f"[{absolute_path}] created")
        else:
            print("[Dataset with this name already exsist], line: 78, module: ", path.basename(__file__))
