import os
import json
import shutil
import getpass
import requests
from bs4 import BeautifulSoup

data = json
URL = "https://elearn.ut.ac.ir/"


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
        user_path = input('Path: ')

    return path, user_path, setup


def write_config(address: str, content: json):
    with open(address, 'w') as config:
        json.dump(content, config, indent=4)


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
        data = init_data
        write_config(os.path.join(path, "config.json"), init_data)

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
        write_config(os.path.join(path, "config.json"), data)

    return path, setup


def print_list():
    if len(data["config"]) == 0:
        print("List is empty")
    else:
        i = 1
        for site in data["config"]:
            print(str(i) + " - Name: " + site["name"] + " , " + "Address: " + site["address"])
            i += 1


def is_available(name="", address="") -> bool:
    for site in data["config"]:
        if site["name"] == name or site["address"] == address:
            return True
    return False


def modify_files(path, add: [], remove: [], load):
    if load == 3:
        files = os.listdir(path)
        files.remove('config.json')
        for file in files:
            os.remove(os.path.join(path, file))
        for i in data["config"]:
            name = i["name"]
            open(os.path.join(path, f'{name}.html'), 'w')
    else:
        add = [x + '.html' for x in add]
        remove = [x + '.html' for x in remove]
        for i in add:
            open(os.path.join(path, i), 'w')
        for j in remove:
            os.remove(os.path.join(path, j))


def modify_list(path, setup):
    choice = 0
    create = []
    delete = []
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
                create.append(name)
            else:
                print("This page is available")

        elif choice == 2:
            number = input("Number: ")
            try:
                if int(number) in range(1, len(data["config"]) + 1):
                    delete.append(data["config"][int(number) - 1]["name"])
                    del data["config"][int(number) - 1]
                else:
                    print("Number not in range")
            except ValueError:
                print('Not valid number')

        print_list()

    write_config(os.path.join(path, "config.json"), data)
    modify_files(path, create, delete, setup)


def confirmation(path, setup):
    confirm = 'x'
    while confirm.upper() != 'Y' and confirm.upper() != 'N':
        confirm = input("Do you confirm ? (Y/N) ")
    if confirm.upper() == 'N':
        modify_list(path, setup)
    elif confirm.upper() == 'Y':
        modify_files(path, [], [], setup)


def check_activity(path):
    username = input("Username: ")
    password = input("Password: ")

    login_request = requests.get(URL)
    session_req = requests.session()
    result = session_req.get(login_request.url)
    parser = BeautifulSoup(result.text, "html.parser")
    execution = parser.find("input", type="hidden")["value"]

    post_data = {'username': username, 'password': password, 'execution': execution,
                 '_eventId': 'submit', 'submit': 'LOGIN', 'geolocation': ''}

    session_req.post(login_request.url, data=post_data, headers=dict(refer=login_request.url))

    print("-----------------------------------------------------------------------------------")
    for site in data["config"]:
        result = session_req.get(site["address"])
        content_parse = BeautifulSoup(result.text, "html.parser")
        content = content_parse.find("div", {"class": "course-content"})
        for s in content.select('input'):
            s.extract()
        name = site["name"]
        file = open(os.path.join(path, f"{name}.html"), 'r', encoding=result.encoding)
        if not str(content) == str(file.read()):
            print(f"Activity on: {name}")
            file.close()
            file = open(os.path.join(path, f"{name}.html"), 'w', encoding=result.encoding)
            file.write(str(content))
    print("-----------------------------------------------------------------------------------")


if __name__ == '__main__':
    print("Hi\nWelcome to E-Learn activity notifier\nIf you want to get notified "
          "about whats going on in course page as soon as possible, you are in right place")

    path, setup = create_setup_files()
    print_list()
    confirmation(path, setup)
    check_activity(path)
