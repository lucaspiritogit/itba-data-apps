import os
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime
import time
from wowtokendag.database_functions import save_to_postgres


def get_oauth_access_token(**kwargs):
    client_id = os.getenv('BATTLE_NET_CLIENT_ID')
    client_secret = os.getenv('BATTLE_NET_CLIENT_SECRET')

    token_url = 'https://oauth.battle.net/token'
    data = {'grant_type': 'client_credentials'}

    response = requests.post(token_url, auth=HTTPBasicAuth(
        client_id, client_secret), data=data)

    if response.status_code == 200:
        access_token = response.json().get('access_token')
        kwargs['ti'].xcom_push(key='access_token', value=access_token)
    else:
        raise Exception(
            f"Failed to fetch access token: {response.status_code}, {response.text}")


def get_wow_token(**kwargs):
    access_token = kwargs['ti'].xcom_pull(
        key='access_token', task_ids='get_oauth_access_token_task')

    if not access_token:
        raise Exception("Access token not found in XCom")

    # Un sleep para no comerme rate limit de parte de la api
    time.sleep(5)

    url = f"https://us.api.blizzard.com/data/wow/token/?namespace=dynamic-us&locale=en_US&access_token={access_token}"
    res = requests.get(url)

    if res.status_code == 200:
        wow_token_price = res.json().get('price')
        last_updated_timestamp_in_ms = res.json().get('last_updated_timestamp')
        last_updated_timestamp = datetime.fromtimestamp(
            last_updated_timestamp_in_ms / 1000)

        execution_date = kwargs['dag_run'].execution_date

        # Divido por 10000 para convertirlo a oro, la moneda principal del juego
        wow_token_price_in_gold = wow_token_price / 10000

        save_to_postgres(execution_date, last_updated_timestamp,
                         wow_token_price_in_gold)

        print(
            f"Data extracted: Execution Date: {execution_date}, Last Updated: {last_updated_timestamp}, Price in Gold: {wow_token_price_in_gold}")
    else:
        raise Exception(
            f"Failed to fetch token: {res.status_code}, {res.text}")
