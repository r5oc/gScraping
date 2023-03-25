from os import path, makedirs
from requests import ConnectionError, ConnectTimeout, get
import shutil


def download_default_file_settings(path_="./settings.json"):

    if not path.isdir("./settings.json"):
        try:
            settings = get(
                "https://raw.githubusercontent.com/r5oc/files-of-requisitions/main/settings.json").content.decode(
                "utf-8")

            with open(path_, "w") as f:
                f.write(settings)
            print(f"{settings} finished downloading")

        except ConnectionError:
            print("Make sure you are connected to the internet to download the default [settings.json]")


def create_snapshot(path_):
    if not path.exists("./snapshots/"):
        makedirs("./snapshots/")

    while True:
        while True:
            snapshot_name = input("Type the name you want to save your snapshot: ")
            if len(snapshot_name) >= 4:
                break
            print("Snapshot name must be at least 4 characters long")

        if not path.isfile(f"./snapshots/{snapshot_name}"):
            shutil.copyfile(path_, f"./snapshots/{snapshot_name}")
            break

        option = input(f"Press 1 to create a snapshot with a different name.\n"
                       f"Press 2 to replace snapshot {snapshot_name}: ")

        if option == "1":
            continue
        elif option == "2":
            shutil.copyfile(path_, f"./snapshots/{snapshot_name}")
            break
        else:
            print("Invalid command try again.")


def restore_snapshot(snapshot_path):
    if not path.isfile(snapshot_path):
        raise FileNotFoundError

    elif path.isfile("./settings.json") and input("Do you want to replace the existing settings.json file?"
                                                  "\nType [yes] if yes or enter to not replace: ").lower() == "yes":
        shutil.copyfile(snapshot_path, r"./settings.json")
        print(f"{snapshot_path} restored to ./settings.json")
    elif not path.isfile("./settings.json"):
        shutil.copyfile(snapshot_path, r"./settings.json")
