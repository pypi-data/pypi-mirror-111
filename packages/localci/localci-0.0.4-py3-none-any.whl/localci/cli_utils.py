import subprocess

from rich.console import Console


def get(command: str) -> str:
    subprocess_result = subprocess.run([command], capture_output=True, text=True, shell=True)
    return str(subprocess_result.stdout).strip()


def call(console: Console, command: str) -> None:
    try:
        subprocess.run([command], capture_output=True, text=True, shell=True, check=True)
    except subprocess.CalledProcessError as exception:
        console.print(exception.stdout)
        console.print(exception.stderr)

        console.print(f'There has been an error with [bold]{command}[/bold], aborting...', highlight=False)
        exit()
