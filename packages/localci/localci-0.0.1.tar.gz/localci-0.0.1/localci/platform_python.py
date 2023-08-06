from typing import Tuple

from .cli_utils import get
from .platform_interface import Platform


class Python(Platform):
    def make(self) -> None:
        with self.console.status("[bold green] Building Maven project...") as status:
            self.check_for_changes(status)

            # Run Python tests
            # status.update(status='Running pytest...')
            # if call('pytest') != 0:
            #     self.console.print("There has been an error with [bold]pytest[/bold]", style="bold red")
            #     exit()

            self.docker_build(status)
            self.docker_push(status, ['latest', self.project_version])
            self.git_push(status)

            status.stop()

        self.print_build_results(['latest', self.project_version])

    def get_project_info(self) -> Tuple[str, str]:
        project_name = get('python setup.py --name')
        project_version = get('python setup.py --version')
        return project_name, project_version
