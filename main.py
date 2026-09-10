import os
import subprocess

import requests
from dotenv import load_dotenv

from model import Repository, Organization

load_dotenv()

GITHUB_PERSONAL_ACCESS_TOKEN = os.getenv('GITHUB_PERSONAL_ACCESS_TOKEN')
ORGANIZATION_NAME = os.getenv('ORGANIZATION_NAME')


def list_organization_repositories(github_personal_access_token: str, organization: str) -> dict:
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': f'Bearer {github_personal_access_token}',
        'X-GitHub-Api-Version': '2026-03-10'
    }
    request = requests.get(f'https://api.github.com/orgs/{organization}/repos', headers=headers)
    return request.json()


def to_organization(organization_name: str, organization_repositories: dict) -> Organization:
    repositories = []
    for repository in organization_repositories:
        repositories.append(Repository(**repository))
    return Organization(**{'name': organization_name, 'repositories': repositories})


def clone_repository(repository: Repository):
    subprocess.run(["./clone_repository.sh", repository.clone_url])


def clone_organization_repositories(organization: Organization):
    for repository in organization.repositories:
        clone_repository(repository)
