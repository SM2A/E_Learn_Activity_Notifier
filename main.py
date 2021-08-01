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
    path, user_path, setup = setup_user()
    if setup == 2 or setup == 4:
        path = os.path.join(path, "E_Learn")
        try:
            os.mkdir(path)
        except FileExistsError:
            shutil.rmtree(path)
            os.mkdir(path)
        init_data = {"config": []}
        with open(os.path.join(path, "config.json"), 'w') as config:
            json.dump(init_data, config, indent=4)
    if setup == 3:
        config_path = os.path.join(user_path, "config.json")
        if os.path.isfile(config_path):
            with open(config_path) as config:
                global data
                data = json.load(config)
                # print(data['config'][1]['address'])
        path = os.path.join(path, "E_Learn")
        try:
            os.mkdir(path)
        except FileExistsError:
            shutil.rmtree(path)
            os.mkdir(path)
        with open(os.path.join(path, "config.json"), 'w') as config:
            json.dump(data, config, indent=4)


if __name__ == '__main__':
    print("Hi\nWelcome to E-Learn activity notifier\nIf you want to get notified "
          "about whats going on in course page as soon as possible, you are in right place")

    create_setup_files()
