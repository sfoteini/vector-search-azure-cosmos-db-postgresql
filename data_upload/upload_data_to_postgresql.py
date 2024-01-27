"""
Creates a new table in the Azure Cosmos DB for PostgreSQL cluster and
populates it with data from the 'dataset/dataset_embeddings.csv' file.

To execute the script, use the following command from the root folder:
`python data_upload/upload_data_to_postgresql.py`

Author: Foteini Savvidou (GitHub @sfoteini)
"""

import os
import psycopg2
from psycopg2 import pool
from dotenv import load_dotenv

# Constants
IMAGE_FILE_COLUMN_NAME = "image_file"
DESCRIPTION_COLUMN_NAME = "description"
AUTHOR_COLUMN_NAME = "author"
TITLE_COLUMN_NAME = "title"
TECHNIQUE_COLUMN_NAME = "technique"
TYPE_COLUMN_NAME = "type"
TIMEFRAME_COLUMN_NAME = "timeframe"
VECTOR_COLUMN_NAME = "vector"

# Directories
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)

# Load environemt file
load_dotenv(os.path.join(parent_dir, ".env"), override=True)
# Azure CosmosDB for PostgreSQL credentials
postgres_host = os.getenv("POSTGRES_HOST")
postgres_database_name = os.getenv("POSTGRES_DB_NAME")
postgres_user = os.getenv("POSTGRES_USER")
postgres_password = os.getenv("POSTGRES_PASSWORD")
sslmode = "require"
table_name = os.getenv("POSTGRES_TABLE_NAME")
postgres_connection_string = (
    f"host={postgres_host} user={postgres_user} "
    f"dbname={postgres_database_name} "
    f"password={postgres_password} sslmode={sslmode}"
)

# Dataset's folder
dataset_folder = os.path.join(parent_dir, "dataset")
dataset_filepath = os.path.join(dataset_folder, "dataset_embeddings.csv")


def main():
    postgresql_pool = psycopg2.pool.SimpleConnectionPool(
        1, 20, postgres_connection_string
    )
    if (postgresql_pool):
        print("Connection pool created successfully")

    # Get a connection from the connection pool
    conn = postgresql_pool.getconn()
    cursor = conn.cursor()

    print("Creating a table...")
    cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
    cursor.execute(
        f"CREATE TABLE {table_name} ("
        f"{IMAGE_FILE_COLUMN_NAME} TEXT PRIMARY KEY,"
        f"{DESCRIPTION_COLUMN_NAME} TEXT NOT NULL,"
        f"{AUTHOR_COLUMN_NAME} TEXT NOT NULL,"
        f"{TITLE_COLUMN_NAME} TEXT NOT NULL,"
        f"{TECHNIQUE_COLUMN_NAME} TEXT,"
        f"{TYPE_COLUMN_NAME} TEXT,"
        f"{TIMEFRAME_COLUMN_NAME} TEXT,"
        f"{VECTOR_COLUMN_NAME} VECTOR(1024) NOT NULL);"
    )

    print("Saving data to table...")
    with open(dataset_filepath) as csv_file:
        cursor.copy_expert(
            f"COPY {table_name} FROM STDIN WITH "
            f"(FORMAT csv, DELIMITER '\t', HEADER MATCH);",
            csv_file
        )

    conn.commit()

    # Fetch all rows from table
    cursor.execute(f"SELECT * FROM {table_name};")
    rows = cursor.fetchall()
    print(f"Number of records in the table: {len(rows)}")

    # Close the connection
    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()
    print("Done!")
