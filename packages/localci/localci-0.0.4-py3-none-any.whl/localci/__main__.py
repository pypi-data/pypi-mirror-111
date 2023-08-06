import argparse

from pyfiglet import Figlet
from rich import get_console

from .platform_angular import Angular
from .platform_mvn import Maven
from .platform_python import Python
from .platform_pypi import Pypi
from .version import __version__


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='local-ci arguments')
    parser.add_argument('platform', type=str, help='Platform for the build process (e.g. mvn, npm, python)')
    return parser.parse_args()


def main():
    args = parse_arguments()

    f = Figlet(font='slant')
    print(f.renderText('local-ci'))

    console = get_console()
    console.print(f'Welcome to [bold]local-ci v{__version__}[/bold]', highlight=False, style='cyan')
    console.line(1)

    if args.platform == 'mvn':
        platform_builder = Maven()
        platform_builder.make()
    elif args.platform == 'python':
        platform_builder = Python()
        platform_builder.make()
    elif args.platform == 'pypi':
        platform_builder = Pypi()
        platform_builder.make()
    elif args.platform == 'angular':
        platform_builder = Angular()
        platform_builder.make()
    else:
        console.print('Invalid platform for the build process.')


if __name__ == '__main__':
    main()
