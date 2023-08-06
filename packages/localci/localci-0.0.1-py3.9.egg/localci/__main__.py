import argparse
from platform import platform

from pyfiglet import Figlet
from .platform_mvn import Maven
from .platform_python import Python


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='local-ci arguments')
    parser.add_argument('platform', type=str, help='Platform for the build process (e.g. mvn, npm, python)')
    return parser.parse_args()


def main():
    args = parse_arguments()

    f = Figlet(font='slant')
    print(f.renderText('local-ci'))

    if args.platform == 'mvn':
        platform_builder = Maven()
        platform_builder.make()
    elif args.platform == 'python':
        platform_builder = Python()
        platform_builder.make()


if __name__ == '__main__':
    main()
