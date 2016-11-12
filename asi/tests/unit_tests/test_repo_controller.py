import unittest
from mock import patch
from asi.controllers import RepoController
from asi.exceptions import UserNotFoundException


class RepoControllerTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch('asi.models.RepoModel.get_user_repos')
    def test_active_user_returns_list(self, mock_get_request):
        expected_repos = [
            {
               'name': 'repo_1',
               'html_url': 'http://github.com/repo_1',
               'size': 1,
            },
        ]
        mock_get_request.return_value = expected_repos
        repos = RepoController.get_public_user_repos('activeuser')
        self.assertEqual(repos, expected_repos)
    
    @patch('asi.models.RepoModel.get_user_repos')
    def test_inactive_user_returns_empty_list(self, mock_get_request):
        mock_get_request.return_value = []
        repos = RepoController.get_public_user_repos('inactiveuser')
        self.assertEqual(repos, [])

    @patch('asi.models.RepoModel.get_user_repos')
    def test_invalid_user_raises_exception(self, mock_get_request):
        mock_get_request.side_effect = UserNotFoundException()
        with self.assertRaises(UserNotFoundException):
            RepoController.get_public_user_repos('notauser')

    @patch('asi.models.RepoModel.get_user_repos')
    def test_result_has_expected_fields(self, mock_get_request):
        github_response = [
            {
               'name': 'repo_1',
               'html_url': 'http://github.com/repo_1',
               'size': 1,
               'private': False,
               'extra_field_1': 'test_1',
               'extra_field_2': 'test_2',
               'extra_field_3': 'test_3',
            },
        ]
        expected_result = [
            {
               'name': 'repo_1',
               'html_url': 'http://github.com/repo_1',
               'size': 1,
            },
        ]
        mock_get_request.return_value = github_response
        repos = RepoController.get_public_user_repos('auser')
        self.assertEqual(repos, expected_result)

    
    @patch('asi.models.RepoModel.get_user_repos')
    def test_results_are_limited(self, mock_get_request):
        github_response = [
            {
               'name': 'repo_1',
               'html_url': 'http://github.com/repo_1',
               'size': 1,
            },
            {
               'name': 'repo_2',
               'html_url': 'http://github.com/repo_2',
               'size': 2,
            },
            {
               'name': 'repo_3',
               'html_url': 'http://github.com/repo_3',
               'size': 3,
            },
            {
               'name': 'repo_4',
               'html_url': 'http://github.com/repo_4',
               'size': 4,
            },
            {
               'name': 'repo_5',
               'html_url': 'http://github.com/repo_5',
               'size': 5,
            },
        ]
        expected_result = [
            {
               'name': 'repo_1',
               'html_url': 'http://github.com/repo_1',
               'size': 1,
            },
            {
               'name': 'repo_2',
               'html_url': 'http://github.com/repo_2',
               'size': 2,
            },
            {
               'name': 'repo_3',
               'html_url': 'http://github.com/repo_3',
               'size': 3,
            },
        ]
        mock_get_request.return_value = github_response
        repos = RepoController.get_public_user_repos('auser', limit=3)
        self.assertEqual(repos, expected_result)


    @patch('asi.models.RepoModel.get_user_repos')
    def test_results_are_ordered_by_size(self, mock_get_request):
        github_response = [
            {
               'name': 'repo_1',
               'html_url': 'http://github.com/repo_1',
               'size': 1,
            },
            {
               'name': 'repo_2',
               'html_url': 'http://github.com/repo_2',
               'size': 2,
            },
            {
               'name': 'repo_3',
               'html_url': 'http://github.com/repo_3',
               'size': 3,
            },
        ]
        expected_result = [
            {
               'name': 'repo_3',
               'html_url': 'http://github.com/repo_3',
               'size': 3,
            },
            {
               'name': 'repo_2',
               'html_url': 'http://github.com/repo_2',
               'size': 2,
            },
            {
               'name': 'repo_1',
               'html_url': 'http://github.com/repo_1',
               'size': 1,
            },
        ]
        mock_get_request.return_value = github_response
        repos = RepoController.get_public_user_repos('auser', orderby='size')
        self.assertEqual(repos, expected_result)
