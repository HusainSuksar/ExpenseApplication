from django.core.management.base import BaseCommand
from django.core.management import call_command
from git import Repo


class Command(BaseCommand):
    help = 'Add Countries to DataBase'

    def handle(self, *args, **kwargs):
        PATH_OF_GIT_REPO = '.git'
        COMMIT_MESSAGE = 'Add AdminLte Static'
        try:
            repo = Repo(PATH_OF_GIT_REPO)
            files = repo.untracked_files
            for i, f in enumerate(files):
                repo.git.add(f)
                print('Add: ' + f)
                if i % 10 == 0:
                    repo.index.commit(COMMIT_MESSAGE)
                    origin = repo.remote(name='origin')
                    origin.push()
                    print('Push')
        except:
            print('Some error occurred while pushing the code')
            call_command('pushStatic')
