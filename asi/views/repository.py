from flask import request
from flask_restful import reqparse, abort, Resource
from requests import codes

from asi.controllers import RepoController
from asi.exceptions import UserNotFoundException


class RepoListView(Resource):
    def get(self):
        limit = request.args.get('limit')
        orderby = request.args.get('orderby', 'size')
        username = request.args.get('username')

        if username is None:
            return 'Bad Request: A username must be specified.', codes.BAD_REQUEST

        try:
            repo_list = RepoController.get_public_user_repos(username, limit=limit, orderby=orderby)
        except UserNotFoundException:
            return 'User {} could not be found'.format(username), codes.NOT_FOUND
        except:
            return 'Internal Server Error', codes.SERVER_ERROR

        return repo_list, codes.OK
