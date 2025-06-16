import git
from app.config import Config

class GitHandler:
    def __init__(self):
        cfg = Config.load()
        self.repo = git.Repo(cfg["vault_path"])
        self.branch = cfg["branch"]

    def pull(self):
        self.repo.remotes.origin.pull(self.branch)

    def commit_and_push(self, message: str):
        self.repo.git.add('--all')
        self.repo.index.commit(message)
        self.repo.remotes.origin.push(self.branch)
