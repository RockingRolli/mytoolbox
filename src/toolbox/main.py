from blessings import Terminal
from toolbox.lib.repositories import init_dir
import click

import locale
locale.setlocale(locale.LC_ALL, 'C.UTF-8')

t = Terminal()

import os

@click.command()
@click.option('-s', default='name', help='Sort list by [name, status, last_commit] - default: name')
@click.option('-f', default=None, help='Filter list by [dirty, clean, nogit] - default: None')
def main(s, f):
    HOME = os.path.expanduser("~")
    DEV_DIR = os.path.join(HOME, 'dev')

    HEAD = '{t.bold}{name:40s}|{status:^9s}|{last_commit_time:^20s}{t.normal}'
    LINE = '{repo.name:40s}|{repo.status_color}{repo.status:^9s}{t.normal}|{repo.last_commit:^20s}'

    print(HEAD.format(t=t, name='Name', status='Status', last_commit_time='Last Commit'))
    print('='*80)

    dirs = os.listdir(DEV_DIR)
    dirs.sort()

    repositories = []

    for directory in os.listdir(DEV_DIR):
        repo_dir = os.path.join(DEV_DIR, directory)

        if not os.path.isdir(repo_dir):
            continue

        r = init_dir(repo_dir)

        repositories.append(r)

    if s not in ['name', 'status', 'last_commit']:
        raise Exception('Invalid filter')

    repositories.sort(key=lambda r: getattr(r, s))

    if f and f in ['clean', 'dirty', 'nogit']:
        repositories = [r for r in repositories if r.status == f]

    for repo in repositories:
        print(LINE.format(t=t, repo=repo))

if __name__ == '__main__':
    main()
