import gc
from json import load, JSONDecodeError

from gScraping.file import *
from os import path


class Settings:
    def __init__(self, path_dictionary="./settings.json"):
        """Constructor"""
        self.path_dictionary = path_dictionary

        self.dictionary = {}
        self.products_dictionary = {}

        self.load_dictionary()
        self.load_product_dictionary()

    def load_dictionary(self):
        try:
            with open(self.path_dictionary, "r") as f:
                self.dictionary = load(f)

        except FileNotFoundError as e:
            print(f"{e} \n[Default file will be downloaded], line: 25")
            download_default_file_settings(self.path_dictionary)

        except JSONDecodeError as e:
            print(f"{e} \n [Json decoder erro], line: 29")

    def load_product_dictionary(self):
        if len(self.dictionary) == 0:
            print("[Dictionary is empty] line: 35, module", path.basename(__file__))
            exit()

        else:
            for item in self.dictionary["products"]:
                self.products_dictionary[item] = []

    def clear_dictionary(self):
        del self.dictionary
        gc.collect()
