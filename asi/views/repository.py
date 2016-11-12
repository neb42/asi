from flask import request
from flask_restful import Resource
from requests import codes

from asi.controllers import RepoController
from asi.exceptions import UserNotFoundException


class RepoListView(Resource):
    def get(self, username):
        limit = int(request.args.get('limit', 5))
        orderby = request.args.get('orderby', 'size')

        try:
            repo_list = RepoController.get_public_user_repos(username, limit=limit, orderby=orderby)
        except UserNotFoundException:
            return 'User {} could not be found'.format(username), codes.NOT_FOUND
        except:
            return 'Internal Server Error', codes.SERVER_ERROR

        return repo_list, codes.OK
