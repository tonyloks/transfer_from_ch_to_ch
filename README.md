transfer_from_ch_to_ch
Этот проект предназначен для переноса данных из одного сервера ClickHouse в другой. Он автоматически создает базы данных и таблицы на целевом сервере и переносит все данные.

Требования
Python 3.6+
Docker
Доступ к исходному и целевому серверам ClickHouse
Установка и настройка
1. Установка Docker
Обновите пакеты:

sudo apt-get update
Установите необходимые пакеты:

sudo apt-get install apt-transport-https ca-certificates curl gnupg lsb-release
Добавьте GPG ключ Docker:

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
Настройте репозиторий:

echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
Установите Docker Engine:

sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
Проверьте установку:

sudo docker run hello-world
2. Развертывание ClickHouse в Docker
Создайте директорию для данных ClickHouse:

sudo mkdir -p /path/to/data
Запустите контейнер ClickHouse:

docker run -d \
    --name some-clickhouse-server \
    --restart=always \
    -p 8123:8123 \
    --ulimit nofile=262144:262144 \
    -v /path/to/data:/var/lib/clickhouse \
    -e CLICKHOUSE_USER=admin \
    -e CLICKHOUSE_PASSWORD=12345m678 \
    clickhouse/clickhouse-server:24.4
Пояснения:

-d: запуск в фоновом режиме
--name: имя контейнера
--restart=always: автоматический перезапуск контейнера
-p 8123:8123: проброс порта HTTP-интерфейса ClickHouse
--ulimit nofile=262144:262144: увеличение лимита открытых файлов
-v /path/to/data:/var/lib/clickhouse: монтирование локальной директории для хранения данных
-e CLICKHOUSE_USER и -e CLICKHOUSE_PASSWORD: задание пользователя и пароля
Проверьте, что контейнер запущен:

docker ps
3. Установка зависимостей Python
Создайте виртуальное окружение:

python -m venv venv
source venv/bin/activate  # На Linux/macOS
venv\Scripts\activate.bat  # На Windows
Установите зависимости:

pip install -r requirements.txt
Использование
Откройте main.py и настройте параметры подключения к исходному и целевому ClickHouse серверам:

python
Copy code
source_client = clickhouse_connect.get_client(host='95.140.154.190', user='default', password='123')
target_client = clickhouse_connect.get_client(host='194.26.232.173', user='admin', password='12345m678')
Запустите скрипт:

python main.py
Скрипт выполнит следующие действия:

Создаст на целевом сервере все базы данных, существующие на исходном (кроме системных).
Создаст все таблицы с идентичной структурой.
Перенесет все данные из исходных таблиц в целевые.
Важные замечания
Скрипт очищает целевые таблицы перед переносом данных.
Системные базы данных (system, INFORMATION_SCHEMA, information_schema) игнорируются.
Данные переносятся чанками по 100,000 строк для эффективности.