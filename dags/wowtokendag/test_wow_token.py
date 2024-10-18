import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from api import fetch_token_for_execution_day


class TestFetchTokenForExecutionDay(unittest.TestCase):

    @patch('api.requests.get')
    @patch('api.save_to_postgres')
    def test_fetch_token_matching_record_found(self, mock_save_to_postgres, mock_requests_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {
                "time": "2024-09-18T02:25:05+00:00",
                "value": 186868
            }
        ]
        mock_requests_get.return_value = mock_response

        execution_date = datetime(2024, 9, 18)

        kwargs = {
            'dag_run': MagicMock(execution_date=execution_date)
        }

        fetch_token_for_execution_day(**kwargs)

        mock_save_to_postgres.assert_called_once_with(
            execution_date, 186868
        )

    @patch('api.requests.get')
    @patch('api.save_to_postgres')
    def test_fetch_token_matching_record_not_found(self, mock_save_to_postgres, mock_requests_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {
                "time": "2024-09-18T02:25:05+00:00",
                "value": 186868
            }
        ]
        mock_requests_get.return_value = mock_response

        execution_date = datetime(2024, 9, 19)

        kwargs = {
            'dag_run': MagicMock(execution_date=execution_date)
        }

        fetch_token_for_execution_day(**kwargs)

        mock_save_to_postgres.assert_not_called()


if __name__ == '__main__':
    unittest.main()
