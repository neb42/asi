from asi.models import RepoModel
from asi.exceptions import UserNotFoundException


class RepoController(object):
    @classmethod
    def get_public_user_repos(cls, username, limit=None, orderby=None):
        # Get repos from model
        repos = RepoModel.get_user_repos(username)

        # Return if no processing needs to be done
        if len(repos) == 0:
            return repos

        # As github explicitly states whether a repo is private (not whether it is public)
        # I am assuming it is public if private is not present
        repos = [k for k in repos if not k.get('private', False)]
        if orderby:
            #TODO: proper sorting algorithm
            repos = sorted(repos, key=lambda k: k[orderby], reverse=True)
        if limit:
            repos = repos[:limit]

        # Select relevant fields
        repos = [{'name': k.get('name'), 'html_url': k.get('html_url'), 'size': k.get('size')} for k in repos]

        return repos
