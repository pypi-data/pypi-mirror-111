import subprocess


def get(command: str) -> str:
    subprocess_result = subprocess.run([command], capture_output=True, text=True, shell=True)
    return str(subprocess_result.stdout).strip()


def call(command: str) -> int:
    subprocess_result = subprocess.run([command], capture_output=True, text=True, shell=True)
    return int(subprocess_result.returncode)
