import requests
from datetime import datetime
import time
from wowtokendag.database_functions import save_to_postgres

class TokenDataFetchError(Exception):
    def __init__(self, status_code, response_text):
        super().__init__(f"Failed to fetch token data: {status_code}, {response_text}")
        self.status_code = status_code
        self.response_text = response_text


def fetch_token_for_execution_day(**kwargs):
    url = "https://data.wowtoken.app/token/history/us/30d.json"
    response = requests.get(url)

    # sleep para no comerme un rate limit
    time.sleep(2)

    if response.status_code == 200:
        data = response.json()
        dag_execution_date = kwargs['dag_run'].execution_date

        matching_record = None
        for record in data:
            record_time = datetime.fromisoformat(
                record['time'].replace("Z", "+00:00"))
            if record_time.date() == dag_execution_date.date():
                matching_record = record
                break

        if matching_record:
            save_to_postgres(
                dag_execution_date, matching_record['value'])
        else:
            print(f"No matching record found for {dag_execution_date.date()}")
    else:
        raise TokenDataFetchError(response.status_code, response.text)
