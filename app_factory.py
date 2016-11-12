from flask import Flask
from flask_restful import Api

from asi.views import RepoListView


ENVIRONMENT_MAP = {
    'DEV': 'config.DevelopmentConfig',
    'TEST': 'config.TestingConfig',
    'PROD': 'config.ProductionConfig',
}


URL_MAP = {
    '/user/<username>/repo/': RepoListView,
}


def build_urls(app):
    api = Api(app)
    for url, resource in URL_MAP.iteritems():
        api.add_resource(resource, url)


def create_app(environment):
    app = Flask(__name__)
    app.config.from_object(ENVIRONMENT_MAP[environment])
    with app.app_context():
        build_urls(app)
    return app


if __name__ == '__main__':
    app = create_app('DEV')
    app.run()
