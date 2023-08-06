import os
from dataclasses import dataclass
from typing import Tuple

from rich import get_console
from rich.prompt import Prompt
from rich.status import Status

from localci.cli_utils import call
from localci.git_utils import tag_exists, changes_exist


@dataclass
class Platform:
    project_name: str
    project_version: str

    def __init__(self):
        self.console = get_console()
        self.project_name, self.project_version = self.get_project_info()

        self.confirmation_dialog()

    @staticmethod
    def get_registry_url() -> str:
        return os.getenv('LOCALCI_REGISTRY_URL', 'registry.sirgje.space')

    def confirmation_dialog(self) -> None:
        # Confirmation dialog for build process
        confirmation = Prompt.ask(f'Building project: {self.application_name}',
                                  choices=["Y", "N"])
        if confirmation != "Y":
            self.console.print("Aborted.", style="bold red")
            exit()

        # Confirmation dialog if git tag already exists
        git_tag_exists = tag_exists(self.project_version)
        if git_tag_exists:
            confirmation = Prompt.ask(f'The git tag {self.project_version} already exists. Proceed?',
                                      choices=["Y", "N"])
            if confirmation != "Y":
                self.console.print("Aborted.", style="bold red")
                exit()

    def make(self) -> None:
        pass

    def get_project_info(self) -> Tuple[str, str]:
        pass

    def check_for_changes(self, status: Status):
        status.update(status='Checking for local repo changes...')
        if changes_exist():
            self.console.print("There are local repo changes that have not been commited!", style="bold red")
            exit()

        self.console.log(':white_check_mark: Checked for local repository changes.')

    def docker_build(self, status: Status, arch: str = 'linux/arm64/v8'):
        status.update(status='Building image with Docker...')
        call(self.console, f'docker buildx build -t {self.application_name} --platform {arch} .')
        self.console.log(':white_check_mark: Built Docker image.')

    def docker_push(self, status: Status, versions: list):
        for version in versions:
            image_with_registry = f'{self.get_registry_url()}/{self.project_name}:{version}'

            status.update(status=f'Tagging docker image for {version}...')
            call(self.console, f'docker tag {self.application_name} {image_with_registry}')
            self.console.log(f':white_check_mark: Tagged Docker image for [bold]{version}[/bold]', highlight=False)

            status.update(status=f'Pushing docker image for {version}...')
            call(self.console, f'docker image push {image_with_registry}')
            self.console.log(f':white_check_mark: Pushed Docker image for [bold]{version}[/bold]', highlight=False)

    def git_push(self, status: Status) -> None:
        status.update(status='Pushing changes to git repository...')
        call(self.console, f'git push')
        self.console.log(':white_check_mark: Pushed changes to git repository.')

    def print_build_results(self, versions: list):
        self.console.line(1)
        self.console.print('[bold]Build process complete![/bold]', style='bold green')

        for version in versions:
            latest_image_uri = f'{self.get_registry_url()}/{self.project_name}:{version}'
            self.console.log(f'[bold]Image:[/bold] {latest_image_uri}', highlight=False)

    @property
    def application_name(self) -> str:
        return f'{self.project_name}:{self.project_version}'
