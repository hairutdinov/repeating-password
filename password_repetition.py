import json
import sys
from werkzeug.security import generate_password_hash, check_password_hash
from getpass import getpass
import random


class PasswordNotFound(Exception): pass
class PasswordIncorrect(Exception): pass
class StopRepetition(Exception): pass


class PasswordRepetition:
    file = 'db.json'

    def __init__(self):
        with open(self.file, 'r') as f:
            self.data = json.load(f)

    def _update_data(self):
        with open('db.json', 'w') as f:
            json.dump(self.data, f)

    def print_list(self):
        print('\n'.join([f'* {name}' for name in self.data.keys()]))

    def add(self, name):
        new_password = {
            name: generate_password_hash(getpass(), method='pbkdf2:sha256', salt_length=8)
        }
        self.data.update(new_password)
        self._update_data()

    def delete(self, name):
        self.data.pop(name)
        self._update_data()

    def start(self, name):
        streak = 0
        password_hash = self.data.get(name)
        if password_hash is None:
            raise PasswordNotFound()
        while True:
            try:
                user_input = getpass('Password or stop: ')
                if user_input.lower() == 'stop':
                    raise StopRepetition()
                if not check_password_hash(password_hash, user_input):
                    raise PasswordIncorrect()
                streak += 1
                print(f'Good! Best streak: {streak}')
            except PasswordIncorrect:
                streak = 0
                print('Try again!')
            except StopRepetition:
                sys.exit()

    def random(self):
        pwd_list = []
        while True:
            if len(pwd_list) == 0:
                pwd_list = list(self.data.keys())[:]

            key = pwd_list.pop(random.randint(0, len(pwd_list)-1))
            password_hash = self.data.get(key)
            print(f'Random: {key}')
            try:
                while True:
                    user_input = getpass(f'[{key}] Password or stop: ')
                    if user_input.lower() == 'stop':
                        raise StopRepetition()
                    if check_password_hash(password_hash, user_input):
                        print()
                        break
                    else:
                        print('Try again!')
            except StopRepetition:
                sys.exit()
