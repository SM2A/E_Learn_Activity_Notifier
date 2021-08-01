import os
import json
import shutil
import getpass

data = json


def setup_user(setup: int = 0):
    while setup != int(1) and setup != int(2) and setup != int(3) and setup != int(4):
        print('1 - Check Activity')
        print('2 - New User')
        print('3 - Load Data')
        print('4 - Reset Data')
        try:
            setup = int(input('Setup: '))
        except ValueError:
            print('Not valid number')

    user_path = ""
    path = f'C:\\Users\\{getpass.getuser()}\\Documents'
    if setup == 3:
        print('Example: \"C:\\Users\\ABC\\Documents\\E_Learn\"')
        user_path = input('Path:')

    return path, user_path, setup


def create_setup_files():
    global data
    path, user_path, setup = setup_user()
    if setup == 1:
        path = os.path.join(path, "E_Learn")
        config_path = os.path.join(path, "config.json")
        if os.path.isfile(config_path):
            with open(config_path) as config:
                data = json.load(config)
    elif setup == 2 or setup == 4:
        path = os.path.join(path, "E_Learn")
        try:
            os.mkdir(path)
        except FileExistsError:
            shutil.rmtree(path)
            os.mkdir(path)
        init_data = {"config": []}
        with open(os.path.join(path, "config.json"), 'w') as config:
            json.dump(init_data, config, indent=4)
    elif setup == 3:
        config_path = os.path.join(user_path, "config.json")
        if os.path.isfile(config_path):
            with open(config_path) as config:
                data = json.load(config)
        path = os.path.join(path, "E_Learn")
        try:
            os.mkdir(path)
        except FileExistsError:
            shutil.rmtree(path)
            os.mkdir(path)
        with open(os.path.join(path, "config.json"), 'w') as config:
            json.dump(data, config, indent=4)

    return path


def print_list():
    i = 1
    for site in data["config"]:
        print(str(i) + " - Name: " + site["name"] + " , " + "Address: " + site["address"])
        i += 1


def is_available(name="", address="") -> bool:
    for site in data["config"]:
        if site["name"] == name or site["address"] == address:
            return True
    return False


def modify_list(path):
    choice = 0
    while choice != int(3):
        print("1 - Add")
        print("2 - Remove")
        print("3 - End Editing")
        try:
            choice = int(input('Input: '))
        except ValueError:
            print('Not valid number')
        if choice == 1:
            name = input("Name: ")
            address = input("Address: ")
            if not is_available(name, address):
                data["config"].append({"name": name, "address": address})
            else:
                print("This page is available")
            print_list()
        elif choice == 2:
            name = input("Name: ")
            for i in range(len(data["config"])):
                if data["config"][i]["name"] == name:
                    del data["config"][i]
                    break
            print_list()
    with open(os.path.join(path, "config.json"), 'w') as config:
        json.dump(data, config, indent=4)


def confirmation(path):
    confirm = 'x'
    while confirm.upper() != 'Y' and confirm.upper() != 'N':
        confirm = input("Do you confirm ? (Y/N) ")
    if confirm.upper() == 'N':
        modify_list(path)


if __name__ == '__main__':
    print("Hi\nWelcome to E-Learn activity notifier\nIf you want to get notified "
          "about whats going on in course page as soon as possible, you are in right place")

    path = create_setup_files()
    print_list()
    confirmation(path)
