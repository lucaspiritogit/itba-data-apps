import requests
from datetime import datetime
import time
from wowtokendag.database_functions import save_to_postgres


def fetch_token_for_execution_day(**kwargs):
    url = "https://data.wowtoken.app/token/history/us/30d.json"
    response = requests.get(url)

    # sleep para no comerme un rate limit
    time.sleep(2)

    if response.status_code == 200:
        data = response.json()
        execution_date = kwargs['dag_run'].execution_date

        matching_record = None
        for record in data:
            record_time = datetime.fromisoformat(
                record['time'].replace("Z", "+00:00"))
            if record_time.date() == execution_date.date():
                matching_record = record
                break

        if matching_record:
            save_to_postgres(
                execution_date, matching_record['value'])
        else:
            print(f"No matching record found for {execution_date.date()}")
    else:
        raise Exception(f"Failed to fetch token data: {
                        response.status_code}, {response.text}")
