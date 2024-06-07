# transfer_from_ch_to_ch

Этот проект предназначен для переноса данных из одного сервера ClickHouse в другой. Он автоматически создает базы данных и таблицы на целевом сервере и переносит все данные.

## Требования

- Python 3.10+
- Docker
- Доступ к исходному и целевому серверам ClickHouse

## Установка и настройка

### 1. Установка Docker

1. Обновите пакеты:
``` bash
sudo apt-get update
```

2. Установите необходимые пакеты:
``` bash
sudo apt-get install apt-transport-https ca-certificates curl gnupg lsb-release
```

3. Добавьте GPG ключ Docker:
``` bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
```

4. Настройте репозиторий:
``` bash
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

5. Установите Docker Engine:
``` bash
sudo apt-get update sudo apt-get install docker-ce docker-ce-cli containerd.io
```

6. Проверьте установку:
``` bash
sudo docker run hello-world
```

### 2. Развертывание ClickHouse в Docker

1. Создайте директорию для данных ClickHouse:
``` bash
sudo mkdir -p /path/to/data
```

2. Запустите контейнер ClickHouse:
``` bash
docker run -d \ --name some-clickhouse-server \ --restart=always \ -p 8123:8123 \ --ulimit nofile=262144:262144 \ -v /path/to/data:/var/lib/clickhouse \ -e CLICKHOUSE_USER=user \ -e CLICKHOUSE_PASSWORD=password \ clickhouse/clickhouse-server:24.4
```

Пояснения:
- `-d`: запуск в фоновом режиме
- `--name`: имя контейнера
- `--restart=always`: автоматический перезапуск контейнера
- `-p 8123:8123`: проброс порта HTTP-интерфейса ClickHouse
- `--ulimit nofile=262144:262144`: увеличение лимита открытых файлов
- `-v /path/to/data:/var/lib/clickhouse`: монтирование локальной директории для хранения данных
- `-e CLICKHOUSE_USER` и `-e CLICKHOUSE_PASSWORD`: задание пользователя и пароля

3. Проверьте, что контейнер запущен:
docker ps


### 3. Установка зависимостей Python

1. Создайте виртуальное окружение:
``` bash
python -m venv venv 
```

2. Запустите окружение
# На Linux/macOS
``` bash
source venv/bin/activate
```

# На Windows
``` bash
venv\Scrips\activate.bat 
```

3. Установите зависимости:
``` bash
pip install -r requirements.txt
```

## Использование

1. Откройте `main.py` и настройте параметры подключения к исходному и целевому ClickHouse серверам:
```python
source_client = clickhouse_connect.get_client(host='1.1.1.1', user='user', password='password')
target_client = clickhouse_connect.get_client(host='2.2.2.2', user='user', password='password')
```
Запустите скрипт:

```
python main.py
```

Скрипт выполнит следующие действия:

- Создаст на целевом сервере все базы данных, существующие на исходном (кроме системных).
- Создаст все таблицы с идентичной структурой.
- Перенесет все данные из исходных таблиц в целевые.


## Важные замечания
Скрипт очищает целевые таблицы перед переносом данных.

Системные базы данных (system, INFORMATION_SCHEMA, information_schema) игнорируются.

Данные переносятся чанками по 100,000 строк для эффективности.