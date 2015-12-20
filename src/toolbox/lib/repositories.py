import os
from git import Repo, InvalidGitRepositoryError
from datetime import datetime
from blessings import Terminal


t = Terminal()


class Directory:
    def __init__(self, path):
        self.working_dir = path

    @property
    def status_color(self):
        return t.white

    @property
    def status(self):
        return 'nogit'

    @property
    def last_commit(self):
        return ''

    @property
    def name(self):
        return os.path.basename(self.working_dir)

    @property
    def active_branch(self):
        return ''


class Repository(Repo):
    @property
    def last_commit(self):
        last_commit_dt = datetime.fromtimestamp(self.head.log()[0].time[0])
        last_commit = last_commit_dt.strftime('%Y-%m-%d %H:%M')
        return last_commit

    @property
    def status_color(self):
        if self.is_dirty():
            return t.red
        else:
            return t.green

    @property
    def status(self):
        if self.is_dirty():
            return 'dirty'
        else:
            return 'clean'

    @property
    def name(self):
        return os.path.basename(self.working_dir)

    @property
    def active_branch(self):
        return self.active_branch.name

def init_dir(path):
    try:
        repo = Repository(path)
    except InvalidGitRepositoryError:
        repo = Directory(path)

    return repo
