from airflow.providers.postgres.hooks.postgres import PostgresHook
import pandas as pd


def create_table():
    postgres_hook = PostgresHook(postgres_conn_id='custom_postgres')
    create_table_query = """
    CREATE TABLE IF NOT EXISTS wow_token_data (
        id SERIAL PRIMARY KEY,
        wow_token_price_in_gold INT NOT NULL,
        start_date TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
        end_date TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
    );
    """
    postgres_hook.run(create_table_query)
    print("Table created successfully.")


def save_to_postgres(execution_date, last_updated_timestamp, wow_token_price_in_gold):
    postgres_hook = PostgresHook(postgres_conn_id='custom_postgres')
    insert_query = """
    INSERT INTO wow_token_data (wow_token_price_in_gold, start_date, end_date)
    VALUES (%s, %s, %s);
    """
    postgres_hook.run(insert_query, parameters=(
        wow_token_price_in_gold, execution_date, last_updated_timestamp))
    print("Data saved successfully.")


def analyze_token_data(**kwargs):
    postgres_hook = PostgresHook(postgres_conn_id='custom_postgres')
    query = "SELECT start_date, wow_token_price_in_gold FROM wow_token_data ORDER BY start_date ASC;"

    connection = postgres_hook.get_conn()
    connection.set_client_encoding('UTF8')
    cursor = connection.cursor()

    try:
        cursor.execute(query)
        rows = cursor.fetchall()
    except UnicodeDecodeError as e:
        print(f"Unicode error: {e}")

    df = pd.DataFrame(rows, columns=['start_date', 'wow_token_price_in_gold'])

    df['price_change'] = df['wow_token_price_in_gold'].diff()

    output_path = '/opt/airflow/output/wow_token_analysis.csv'
    df.to_csv(output_path, index=False, encoding='utf-8')
    print(f"Analysis complete. Data saved to {output_path}")
    return df
