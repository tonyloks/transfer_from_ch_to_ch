import clickhouse_connect

# Подключение к исходному ClickHouse серверу
source_client = clickhouse_connect.get_client(host='1.1.1.1', user='user', password='password')

# Подключение к целевому ClickHouse серверу
target_client = clickhouse_connect.get_client(host='2.2.2.2', user='user', password='password')


def create_databases(source_client, target_client):
    # Получение списка баз данных
    databases_result = source_client.query('SHOW DATABASES')
    databases = [database[0] for database in databases_result.result_set]

    # Список системных баз данных в ClickHouse
    system_databases = ['system', 'INFORMATION_SCHEMA', 'information_schema']

    # Фильтрация списка баз данных, исключая системные
    databases = [db for db in databases if db not in system_databases]

    for database_name in databases:
        print(f"Обработка базы данных: {database_name}")

        # Создание базы данных на целевом сервере
        target_client.command(f"CREATE DATABASE IF NOT EXISTS {database_name}")

    return databases

def create_tables(source_client, target_client, databases):
    for database_name in databases:
        # Получение списка таблиц в базе данных
        tables_result = source_client.query(f"SHOW TABLES FROM {database_name}")
        tables = [table[0] for table in tables_result.result_set]

        for table_name in tables:
            print(f"  Обработка таблицы: {table_name}")

            # Проверка существования таблицы на целевом сервере
            target_client.command(f"USE {database_name}")
            table_exists = target_client.query(f"EXISTS TABLE {table_name}").result_rows[0][0]

            if not table_exists:
                # Получение структуры таблицы
                table_structure = source_client.query(f"SHOW CREATE TABLE {database_name}.{table_name}")
                create_table_query = table_structure.result_rows[0][0]

                # Создание таблицы на целевом сервере
                target_client.command(create_table_query)
            else:

                print(f"    Таблица {table_name} уже существует на целевом сервере в базе {database_name}")


def transfer_data(source_client, target_client, databases, tables, chunk_size=100000):
    for database_name in databases:
        for table_name in tables[database_name]:
            print(f"  Перенос данных из таблицы: {database_name}.{table_name}")

            # Перенос данных из исходной таблицы в целевую
            source_client.command(f"USE {database_name}")
            target_client.command(f"USE {database_name}")

            # Очистка целевой таблицы
            target_client.command(f"TRUNCATE TABLE {table_name}")

            # Выгрузка и вставка данных чанками
            offset = 0
            while True:
                data = source_client.query(f"SELECT * FROM {table_name} LIMIT {chunk_size} OFFSET {offset}")
                if not data.result_rows:
                    break
                target_client.insert(table_name, data.result_rows)
                offset += chunk_size

# Создание баз данных и получение их списка
databases = create_databases(source_client, target_client)

# Создание словаря таблиц
tables = {}
for database_name in databases:
    tables_result = source_client.query(f"SHOW TABLES FROM {database_name}")
    tables[database_name] = [table[0] for table in tables_result.result_set]

# Создание таблиц
create_tables(source_client, target_client, databases)

# Перенос данных
transfer_data(source_client, target_client, databases, tables)