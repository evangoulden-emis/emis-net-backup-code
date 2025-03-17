from typing import Any

import github
import yaml
from github import Github
import os

from github.Repository import Repository


def get_github_instance() -> set[Github | Repository | Any] | None:
    with open('github.yaml') as f:
        content = yaml.safe_load(f)
        g = Github(content['secrets']['token'])
        repo = g.get_repo(content['repo'])
        backup_dir = content['backup_dir']
        return {g, repo, backup_dir}


def upload_file_to_github(g, repo, backup_dir):
    files = [f for f in os.listdir(backup_dir) if f.endswith('.txt')]
    for f in files:
        with open(f"{backup_dir}/{f}", 'r') as file:
            content = file.read()
            try:
                file_contents = repo.get_contents(f)
                repo.update_file(f, f"Updating backup for {f}", content, file_contents.sha, branch="main")
            except github.UnknownObjectException:
                repo.create_file(f, f"Adding backup for {f}", content, branch="main")




