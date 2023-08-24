import sys
import argparse
import password_repetition
from password_repetition import PasswordRepetition

parser = argparse.ArgumentParser(description='Remember password')

parser.add_argument('-s', '--save', type=str, help='Give password name and save', metavar='name', nargs='?')
parser.add_argument('-c', '--choose', type=str, help='Choose password by name', metavar='name', nargs='?')
parser.add_argument('-d', '--delete', type=str, help='Delete password by name', metavar='name', nargs='?')
parser.add_argument('-l', '--list', action='store_true', help='List password names')
parser.add_argument('-r', '--random', action='store_true', help='Get random password')

args = parser.parse_args()

pr = PasswordRepetition()

if args.list:
    pr.print_list()
elif args.save:
    pr.add(args.save)
elif args.delete:
    pr.delete(args.delete)
elif args.choose:
    try:
        pr.start(args.choose)
    except password_repetition.PasswordNotFound:
        print("There is no such an item")
        sys.exit()
elif args.random:
    pr.random()