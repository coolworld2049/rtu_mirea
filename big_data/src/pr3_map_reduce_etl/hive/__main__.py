import argparse

from loguru import logger
from pyhive import hive

hive_host = "localhost"
hive_port = 10000
hive_username = "user"
hive_password = "password"
hive_database = "hivedb"

connection = hive.Connection(
    host=hive_host,
    port=hive_port,
    username=hive_username,
    password=hive_password,
    database=hive_database,
)

cursor = connection.cursor()


def hql_exec(hql_file_path):
    try:
        with open(hql_file_path, "r") as sql_file:
            hive_commands = sql_file.read().split(";")
        for command in hive_commands:
            if command.strip():
                cursor.execute(command)
        connection.commit()
        logger.info("Hive commands executed successfully from file.")
    except Exception as e:
        logger.error(f"Error executing Hive commands: {e}")
    finally:
        connection.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--hql_file_path", required=True)
    args = parser.parse_args()
    exec(args.hql_file_path)
