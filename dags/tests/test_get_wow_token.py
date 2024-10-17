import unittest
from unittest.mock import MagicMock
from wowtokendag.battle_net_api import get_wow_token


class TestGetWowToken(unittest.TestCase):

    def test_get_wow_token_no_access_token(self):
        mock_context = {
            'ti': MagicMock(),
            'dag_run': MagicMock()
        }
        mock_context['ti'].xcom_pull.return_value = None

        with self.assertRaises(Exception) as context:
            get_wow_token(**mock_context)

        self.assertEqual(str(context.exception),
                         "Access token not found in XCom")


if __name__ == '__main__':
    unittest.main()
