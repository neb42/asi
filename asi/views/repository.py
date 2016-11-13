from flask import request
from flask_restful import Resource
from requests import codes

from asi.controllers import RepoController
from asi.exceptions import UserNotFoundException


class RepoListView(Resource):
    def get(self, username):
        orderby = request.args.get('orderby', 'size')
        limit = request.args.get('limit', 5)
        try:
            limit = int(limit)
        except ValueError:
            return 'Bad Request: limit must be an integer.', codes.BAD_REQUEST

        if limit < 1:
            return 'Bad Request: you have requested to view no repositories.', codes.BAD_REQUEST

        try:
            repo_list = RepoController.get_public_user_repos(username, limit=limit, orderby=orderby)
        except UserNotFoundException:
            return 'User {} could not be found'.format(username), codes.NOT_FOUND
        except:
            return 'Internal Server Error', codes.SERVER_ERROR

        return repo_list, codes.OK
