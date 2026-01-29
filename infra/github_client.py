from typing import Set
from github import Github, GithubException

from infra.settings import settings
from utils.constants import REQUIRED_SUBFOLDERS
from logger.logging import configure_logging

logger = configure_logging()

_github: Github | None = None

def get_github_client() -> Github:
    global _github
    if _github is None:
        _github = Github(settings.github_token)
    return _github

def validate_project_structure(owner: str, repository: str, ref: str) -> None:
    """
    Valida que:
    - el repositorio exista
    - el ref exista (branch/tag/commit)
    - en la raíz existan REQUIRED_SUBFOLDERS
    """
    github = get_github_client()
    full_name = f"{owner}/{repository}"

    try:
        repo = github.get_repo(full_name)
    except GithubException:
        logger.warning(f"Repositorio no encontrado: {full_name}")
        raise ValueError("Project not found")

    # Validar ref → resolvemos a commit
    try:
        commit = repo.get_commit(ref)
    except GithubException:
        logger.warning(f"Ref no encontrado: {ref} en {full_name}")
        raise ValueError("Ref not found")

    # Tree raíz (no recursivo)
    tree = repo.get_git_tree(commit.sha, recursive=False)

    found: Set[str] = set()
    for element in tree.tree:
        if element.type == "tree":
            folder = f"{element.path}/"
            if folder in REQUIRED_SUBFOLDERS:
                found.add(folder)

    if found != REQUIRED_SUBFOLDERS:
        missing = sorted(list(REQUIRED_SUBFOLDERS - found))
        logger.warning(f"Estructura inválida en {full_name}@{ref}, faltan: {missing}")
        raise ValueError(f"Required folders not found: {missing}")

    logger.info(f"Validación OK para {full_name}@{ref}")
