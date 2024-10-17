from unittest.mock import patch, MagicMock
from wowtokendag.battle_net_api import get_oauth_access_token
import requests
import os
import unittest


class TestGetOAuthAccessToken(unittest.TestCase):

    @patch('requests.post')
    @patch('os.getenv')
    @patch('airflow.models.taskinstance.TaskInstance.xcom_push')
    def test_get_oauth_access_token_success(self, mock_xcom_push, mock_getenv, mock_post):
        mock_getenv.side_effect = lambda key: {'BATTLE_NET_CLIENT_ID': 'fake_client_id',
                                               'BATTLE_NET_CLIENT_SECRET': 'fake_client_secret'}.get(key)
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'access_token': 'fake_access_token'}
        mock_post.return_value = mock_response

        mock_task_instance = MagicMock()
        mock_context = {'ti': mock_task_instance}

        get_oauth_access_token(**mock_context)

        mock_post.assert_called_once_with(
            'https://oauth.battle.net/token',
            auth=requests.auth.HTTPBasicAuth(
                'fake_client_id', 'fake_client_secret'),
            data={'grant_type': 'client_credentials'}
        )

        mock_task_instance.xcom_push.assert_called_once_with(
            key='access_token', value='fake_access_token')


if __name__ == '__main__':
    unittest.main()
