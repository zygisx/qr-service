import argparse


def main():
    parser = argparse.ArgumentParser(description='Manage this Flask application.')
    parser.add_argument('command', help='the name of the command you want to run')
    args = parser.parse_args()

    if args.command == 'create_db':
        print "DB created!"
    elif args.command == 'delete_db':
        print "DB deleted!"
    else:
        raise Exception('Invalid command')


if __name__ == '__main__':
    main()



