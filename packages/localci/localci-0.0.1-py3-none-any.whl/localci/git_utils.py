import subprocess


def changes_exist() -> bool:
    git_status = subprocess.check_output(['git', 'status', '-s'])
    return len(git_status) > 0


def tag_exists(tag_name: str) -> bool:
    try:
        git_tag = subprocess.check_output(f'git tag | grep {tag_name}', shell=True)
        return len(git_tag) > 0
    except subprocess.CalledProcessError:
        return False


def push() -> bool:
    git_push = subprocess.run(['git', 'push'])
    return git_push.returncode == 0
