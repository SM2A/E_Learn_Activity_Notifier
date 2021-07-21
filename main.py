import getpass

if __name__ == '__main__':

    print("Hi\nWelcome to E-Learn activity notifier\nIf you want to get notified"
          "about whats going on in course page as soon as possible, you are in right place")

    setup: int = 0
    while setup != int(1) and setup != int(2) and setup != int(3) and setup != int(4):
        print('1 - Check Activity')
        print('2 - New User')
        print('3 - Load Data')
        print('4 - Reset Data')
        try:
            setup = int(input('Setup: '))
        except ValueError:
            print('Not valid number')

    path = ''
    if setup == 3:
        print('Example: \"C:\\Users\\ABC\\Documents\"')
        path = input('Path:')
    else:
        path = f'C:\\Users\\{getpass.getuser()}\\Documents'

