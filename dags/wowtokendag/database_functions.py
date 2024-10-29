from airflow.providers.postgres.hooks.postgres import PostgresHook
import pandas as pd
import logging
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()


def get_redshift_connection():
    conn = None
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("REDSHIFT_DBNAME"),
            user=os.getenv("REDSHIFT_USER"),
            password=os.getenv("REDSHIFT_PASSWORD"),
            host=os.getenv("REDSHIFT_HOST"),
            port=os.getenv("REDSHIFT_PORT")
        )
        print("Connection to redshift successful.")
    except Exception as e:
        print(f"Connection to redshift failed: {e}")
    return conn


def create_table():
    create_table_query = """
    CREATE TABLE IF NOT EXISTS "2024_lucas_ignacio_pirito_schema".wow_token_data (
        id INT IDENTITY(1,1) PRIMARY KEY,
        wow_token_price_in_gold INT NOT NULL,
        token_price_date TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
    );
    """
    connection = None
    try:
        connection = get_redshift_connection()
        with connection.cursor() as cursor:
            cursor.execute(create_table_query)
        connection.commit()
    except Exception as e:
        logging.error(f"Error creating table: {e}")
    finally:
        connection.close()


def save_to_postgres(execution_date, wow_token_price_in_gold):
    insert_query = """
    INSERT INTO "2024_lucas_ignacio_pirito_schema".wow_token_data (wow_token_price_in_gold, token_price_date)
    VALUES (%s, %s);
    """
    connection = None
    try:
        connection = get_redshift_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                insert_query, (wow_token_price_in_gold, execution_date))
        connection.commit()
    except Exception as e:
        logging.error(f"Error inserting data: {e}")
    finally:
        connection.close()


def analyze_token_data():
    query = """
    SELECT token_price_date, wow_token_price_in_gold FROM "2024_lucas_ignacio_pirito_schema".wow_token_data ORDER BY token_price_date ASC;
    """
    connection = None
    try:
        connection = get_redshift_connection()
        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
    except UnicodeDecodeError as e:
        logging.error(f"Unicode error: {e}")
        raise UnicodeDecodeError
    except Exception as e:
        logging.error(
            f"Unexpected error while fetching data from Redshift: {e}")
        raise ConnectionError(
            f"Unexpected error while fetching data from Redshift: {e}")
    finally:
        connection.close()

    df = pd.DataFrame(
        rows, columns=['token_price_date', 'wow_token_price_in_gold'])
    df['price_change'] = df['wow_token_price_in_gold'].diff().fillna(0)

    output_path = '/opt/airflow/output/wow_token_analysis.csv'
    df.to_csv(output_path, index=False, encoding='utf-8')
    return df
