from typing import Tuple

from rich import *
from rich.prompt import Prompt

from .platform_interface import Platform
from .git_utils import changes_exist, tag_exists
from .cli_utils import get, call


class Python(Platform):
    def make(self) -> None:
        console = get_console()

        self.project_name, self.project_version = self.get_project_info()
        application_name = f'{self.project_name}:{self.project_version}'

        # Confirmation dialog for build process
        confirmation = Prompt.ask(f'Building Python project: {application_name}',
                                  choices=["Y", "N"])
        if confirmation != "Y":
            console.print("Aborted.", style="bold red")
            exit()

        # Confirmation dialog if git tag already exists
        git_tag_exists = tag_exists(self.project_version)
        if git_tag_exists:
            confirmation = Prompt.ask(f'The git tag {self.project_version} already exists. Proceed?',
                                      choices=["Y", "N"])
            if confirmation != "Y":
                console.print("Aborted.", style="bold red")
                exit()

        with console.status("[bold green] Building Maven project...") as status:
            # Check for local repo changes
            status.update(status='Checking for local repo changes...')
            if changes_exist():
                console.print("There are local repo changes that have not been commited!", style="bold red")
                exit()

            console.log(':white_check_mark: Checked for local repository changes.')

            # Run Python tests
            status.update(status='Running pytest...')
            if call('pytest') != 0:
                console.print("There has been an error with [bold]pytest[/bold]", style="bold red")
                exit()

            # Build with docker
            status.update(status='Building image with Docker...')
            if call(f'docker buildx build -t {application_name} --platform linux/arm64/v8 .') != 0:
                console.print("There has been an error with [bold]docker buildx[/bold]", style="bold red")
                exit()

            console.log(':white_check_mark: Built Docker image.')

            # Tag and push docker images
            docker_registry_url = 'registry.sirgje.space'

            status.update(status='Tagging docker images...')
            if call(f'docker tag {application_name} {docker_registry_url}/{self.project_name}:latest') != 0:
                console.print("There has been an error with [bold]docker tag[/bold]", style="bold red")
                exit()

            console.log(':white_check_mark: Tagged Docker images.')

            status.update(status='Pushing docker images...')
            if call(f'docker image push {docker_registry_url}/{self.project_name}:latest') != 0:
                console.print("There has been an error with [bold]docker push[/bold]", style="bold red")
                exit()

            console.log(':white_check_mark: Pushed Docker images.')

            status.update(status='Pushing changes to git repository...')
            if call(f'git push') != 0:
                console.print("There has been an error with [bold]git push[/bold]", style="bold red")
                exit()

            console.log(':white_check_mark: Pushed changes to git repository.')
            status.stop()

    def get_project_info(self) -> Tuple[str, str]:
        project_name = get('python setup.py --name')
        project_version = get('python setup.py --version')
        return project_name, project_version
