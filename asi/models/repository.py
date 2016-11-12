import urllib
import requests

from asi.exceptions import UserNotFoundException, HTTP500Exception


class RepoModel(object):
    base_url = 'https://api.github.com'
    headers = {
        "Accept": "application/vnd.github.v3+json"
    }

    @classmethod
    def get_user_repos(cls, username):
        url = '{}/users/{}/repos'.format(cls.base_url, urllib.quote(username))
        response = requests.get(url, headers=cls.headers)
        if response.status_code == requests.codes.NOT_FOUND:
            raise UserNotFoundException()
        elif response.status_code == requests.codes.OK:
            return response.json()
        else:
            raise HTTP500Exception() 
