import os
from typing import Tuple

from .cli_utils import call
from .cli_utils import get
from .platform_interface import Platform


class Pypi(Platform):
    def login_dialog(self) -> None:
        self.username = self.console.input('Enter your [bold]pypi.org[/bold] username: ')
        self.password = self.console.input('Enter your [bold]pypi.org[/bold] password: ', password=True)

        os.putenv('TWINE_USERNAME', self.username)
        os.putenv('TWINE_PASSWORD', self.password)

    def make(self) -> None:
        with self.console.status("[bold green] Building pypi package...") as status:
            self.check_for_changes(status)

            # Build Python package
            status.update(status='Building pypi package...')
            call(self.console, 'python setup.py sdist bdist_wheel')
            call(self.console, 'twine check dist/*')
            self.console.log(':white_check_mark: Built pypi package!')

            status.update(status='Uploading to pypi...')
            call(self.console, f'twine upload --non-interactive dist/*')
            self.console.log(':white_check_mark: Uploaded package to pypi!')

            self.git_push(status)

            status.stop()

        self.print_build_results([self.project_version])

    def print_build_results(self, versions: list):
        self.console.line(1)
        self.console.print('[bold]Build process complete![/bold]', style='bold green')

        for _ in versions:
            self.console.log(f'[bold]Package:[/bold] {self.project_name}==={self.project_version}', highlight=False)

    def get_project_info(self) -> Tuple[str, str]:
        project_name = get('python setup.py --name')
        project_version = get('python setup.py --version')
        return project_name, project_version
