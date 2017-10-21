import sys

from vkservices import main


def print_usage():
    print('Usage: manage.py runserver')
    exit(-1)

if len(sys.argv) == 1:
    print_usage()

command = sys.argv[1]

if command == 'runserver':
    sys.argv.pop(1)
    main.main()
else:
    print_usage()
