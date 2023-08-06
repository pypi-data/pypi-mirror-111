from typing import Tuple

from .cli_utils import call
from .cli_utils import get
from .platform_interface import Platform


class Angular(Platform):
    def make(self) -> None:
        with self.console.status("[bold green] Building Angular project...") as status:
            self.check_for_changes(status)

            # Build with Angular
            status.update(status='Installing npm dependencies...')
            call(self.console, '~/.nvm/nvm.sh use')  # This needs chmod +x, hacky!
            call(self.console, 'npm install')
            self.console.log(':white_check_mark: Installed npm dependencies.')

            status.update(status='Building Angular application...')
            call(self.console, 'ng build --outputPath=./build/dist')
            self.console.log(':white_check_mark: Built application with Angular.')

            self.docker_build(status)
            self.docker_push(status, ['latest', self.project_version])
            self.git_push(status)

            status.stop()

        self.print_build_results(['latest', self.project_version])

    def get_project_info(self) -> Tuple[str, str]:
        project_name = get('node -e "console.log(require(\'./package.json\').name)"')
        project_version = get('node -e "console.log(require(\'./package.json\').version)"')
        return project_name, project_version
