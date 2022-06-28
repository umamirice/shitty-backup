#!/usr/bin/env python3
# Usage is very straightforward
# Config file consists of 3 elements
# First line (from_path) path from recursively backup will be created using rsync
# Second line (to_path) path to which our program will write all the files
# Third and every next line starting with ex is for exclusions
# since rsync syntax forces us to repetitively add --exclude flags
from os import getcwd, system
from typing import List
from time import sleep
from colorama import Fore
from colorama import Style

global from_path, to_path, exclude
config_path: str = str(getcwd()) + "/backup.conf"


class Backup:
    def __init__(self, fp: str, tp: str, exc: list[str]) -> None:
        if exc is None:
            exc = exclude
        self.from_path = fp
        self.to_path = tp
        self.exclude = exc
        self.zip = ""
        self.rsync = ""
        pass

    def make_backup(self) -> None:
        print("Do you want to create a mirror backup?")
        print(f"{Fore.RED}WARNING! IT WILL DELETE ALL FILES IN{Style.RESET_ALL} {self.to_path}")
        mirror = input("y/n: ")

        # Creating the actual backup command
        self.rsync = "rsync -aAXv"
        if mirror.upper() == "Y":
            self.rsync += " --delete"
        for i in self.exclude:
            self.rsync += f" --exclude=\"{i}\""
        self.rsync += f" {self.from_path}"
        self.rsync += f" {self.to_path}"
        pass

    def zip_backup(self) -> None:
        path_to_zip = input("Where do you want to zip the backup? [enter for the same name as path to backup]: ")
        if path_to_zip == "":
            path_to_zip = self.to_path
        self.zip = f"zip -1 -u -T -r {path_to_zip}.zip {self.to_path}"
        pass

    def write(self) -> None:
        print(f"Creating backup using\n\t{self.rsync}\n")
        print(f"Zipping the backup using\n\t{self.zip}\n")
        write: str = input("Are your ready to write these changes to disk? y/n: ")
        if write.upper() == "Y":
            print("Backup will start in a second...")
            sleep(4)
            system(self.rsync)
            system(self.zip)
            print(f"Succesfully saved backup at {self.to_path}")
            print(f"and zip at {path_to_zip}")
        pass


print("1. Config file path")
print("2. Config manually")
option: int = 0
try:
    option = int(input("> "))
except (TypeError, ValueError):
    print("What the fuck bro")
    exit(0)
try:
    if option == 1:
        print("Using file config")
        tmp: str = input(f"Enter absolute path for config file [{config_path}] or enter to use default: ")
        if tmp != "":
            config_path = tmp
        try:
            f = open(config_path, 'r')
            f.close()
        except FileNotFoundError:
            print("File doesn\'t exist")
            exit()

        config = open(config_path, 'r')

        from_path = config.readline().rstrip("\n")
        to_path = config.readline().rstrip("\n")

        exclude = []
        for i in config:
            if i[0:2] == "ex":
                exclude.append(i.lstrip("ex ").rstrip("\n"))

    elif option == 2:
        print("Starting manual config...")
        from_path: str = input("Enter absolute path of files you wanna backup: ")
        to_path: str = input("Enter directory where you wanna have your backup: ")
        exclude: list[str] = []

        do_exclude = input("Do you wanna exclude files/directories? y/n: ")
        if do_exclude.upper() == "Y":
            while True:
                tmp = input("Enter excluded files/directories (one per line) q to quit: ")
                if tmp == "q":
                    break
                exclude.append(tmp)

        print(f"From: {from_path}")
        print(f"To  : {to_path}")
        print("Exclude:", end=" ")
        for i in exclude:
            print(i, end=" ")
        print()

        save_config = input("Do you want to save this configuration? y/n: ")
        if save_config.upper() == "Y":
            filename = input("Enter name of configuration file without extension: ")
            f = open(getcwd() + f"/{filename}.conf", 'w')
            f.write(f"{from_path}\n")
            f.write(f"{to_path}\n")
            for i in exclude:
                f.write(f"ex {i}\n")
            f.close()
            print(f"Saved at {getcwd()}/{filename}.conf")
    else:
        raise ValueError
except ValueError:
    print("Wrong option mate")

backup = Backup(from_path, to_path, exclude)
backup.make_backup()
backup.zip_backup()
backup.write()
