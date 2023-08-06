from typing import Tuple

from .cli_utils import get, call
from .platform_interface import Platform


class Maven(Platform):
    def make(self) -> None:
        with self.console.status("[bold green] Building Maven project...") as status:
            self.check_for_changes(status)

            # Build with maven
            status.update(status='Building application package with Maven...')
            call('mvn clean package')

            self.console.log(':white_check_mark: Built application package with Maven.')

            self.docker_build(status)
            self.docker_push(status, ['latest', self.project_version])
            self.git_push(status)
            status.stop()

        self.print_build_results(['latest', self.project_version])

    def get_project_info(self) -> Tuple[str, str]:
        project_name = get('mvn help:evaluate -Dexpression=project.name -q -DforceStdout')
        project_version = get('mvn help:evaluate -Dexpression=project.version -q -DforceStdout')
        return project_name, project_version
