from git import Repo


class GitSupport:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.repo = None

    def check_init(self):
        """check repo is initialized"""
        assert self.repo

    def init_repo(self, path, bare=False):
        """init git repo in given path"""
        repo = Repo.init(path=path, bare=bare)
        self.repo = repo
        return repo

    def commit_file(self, file_path, commit_message):
        """add file & commit it"""
        self.check_init()
        self.repo.index.add([file_path])
        self.repo.index.commit(commit_message)
