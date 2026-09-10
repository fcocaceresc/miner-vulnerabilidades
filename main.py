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


def clone_repository(repository: Repository, directory: str):
    full_directory = os.path.join(directory, repository.name)
    if os.path.exists(full_directory):
        return
    subprocess.run(["./clone_repository.sh", repository.clone_url, full_directory])


def clone_organization_repositories(organization: Organization):
    for repository in organization.repositories:
        clone_repository(repository, organization.name)


def language_to_identifier(language: str | None) -> str | None:
    mapper = {
        'C/C++': 'c-cpp',
        'C#': 'csharp',
        'GitHub Actions workflows': 'actions',
        'Go': 'go',
        'Java/Kotlin': 'java-kotlin',
        'JavaScript/TypeScript': 'javascript-typescript',
        'Python': 'python',
        'Ruby': 'ruby',
        'Rust': 'rust',
        'Swift': 'swift'
    }
    return mapper.get(language, None)


def create_codeql_database(repository: Repository, path_to_database: str, source_root: str):
    language_identifier = language_to_identifier(repository.language)
    if language_identifier is None:
        return
    subprocess.run(['./codeql_database_create.sh', path_to_database, language_identifier, source_root])


def create_codeql_databases(organization: Organization):
    for repository in organization.repositories:
        path_to_database = f'./codeql_databases/{organization.name}/{repository.name}'
        os.makedirs(path_to_database, exist_ok=True)
        create_codeql_database(repository, path_to_database, os.path.join(organization.name, repository.name))
