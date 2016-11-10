import urllib
import requests

from asi.exceptions import UserNotFoundException


class RepoController(object):
    base_url = 'https://api.github.com'

    @classmethod
    def get_public_user_repos(cls, username, limit=None, orderby=None):
        url = '{}/users/{}/repos'.format(cls.base_url, urllib.quote(username))
        headers = {
            "Accept": "application/vnd.github.v3+json"
        }
        response = requests.get(url, headers=headers)

        if response.status_code == requests.codes.NOT_FOUND:
            raise UserNotFoundException()

        result = response.json()

        if len(result) == 0:
            return result

        result = [k for k in result if not k['private']]
        if orderby:
            #TODO: proper sorting algorithm
            result = sorted(result, key=lambda k: k[orderby], reverse=True)
        if limit:
            result = result[:limit]

        result = [{'name': k['name'], 'html_url': k['html_url'], 'size': k['size']} for k in result]

        return result
