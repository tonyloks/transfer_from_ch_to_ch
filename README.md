# transfer_from_ch_to_ch

���� ������ ������������ ��� �������� ������ �� ������ ������� ClickHouse � ������. �� ������������� ������� ���� ������ � ������� �� ������� ������� � ��������� ��� ������.

## ����������

- Python 3.10+
- Docker
- ������ � ��������� � �������� �������� ClickHouse

## ��������� � ���������

### 1. ��������� Docker

1. �������� ������:
``` bash
sudo apt-get update
```

2. ���������� ����������� ������:
``` bash
sudo apt-get install apt-transport-https ca-certificates curl gnupg lsb-release
```

3. �������� GPG ���� Docker:
``` bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
```

4. ��������� �����������:
``` bash
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

5. ���������� Docker Engine:
``` bash
sudo apt-get update sudo apt-get install docker-ce docker-ce-cli containerd.io
```

6. ��������� ���������:
``` bash
sudo docker run hello-world
```

### 2. ������������� ClickHouse � Docker

1. �������� ���������� ��� ������ ClickHouse:
``` bash
sudo mkdir -p /path/to/data
```

2. ��������� ��������� ClickHouse:
``` bash
docker run -d \ --name some-clickhouse-server \ --restart=always \ -p 8123:8123 \ --ulimit nofile=262144:262144 \ -v /path/to/data:/var/lib/clickhouse \ -e CLICKHOUSE_USER=user \ -e CLICKHOUSE_PASSWORD=password \ clickhouse/clickhouse-server:24.4
```

���������:
- `-d`: ������ � ������� ������
- `--name`: ��� ����������
- `--restart=always`: �������������� ���������� ����������
- `-p 8123:8123`: ������� ����� HTTP-���������� ClickHouse
- `--ulimit nofile=262144:262144`: ���������� ������ �������� ������
- `-v /path/to/data:/var/lib/clickhouse`: ������������ ��������� ���������� ��� �������� ������
- `-e CLICKHOUSE_USER` � `-e CLICKHOUSE_PASSWORD`: ������� ������������ � ������

3. ���������, ��� ��������� �������:
docker ps


### 3. ��������� ������������ Python

1. �������� ����������� ���������:
``` bash
python -m venv venv 
```

2. ��������� ���������
# �� Linux/macOS
``` bash
source venv/bin/activate
```

# �� Windows
``` bash
venv\Scrips\activate.bat 
```

3. ���������� �����������:
``` bash
pip install -r requirements.txt
```

## �������������

1. �������� `main.py` � ��������� ��������� ����������� � ��������� � �������� ClickHouse ��������:
```python
source_client = clickhouse_connect.get_client(host='1.1.1.1', user='user', password='password')
target_client = clickhouse_connect.get_client(host='2.2.2.2', user='user', password='password')
```
��������� ������:

```
python main.py
```

������ �������� ��������� ��������:

- ������� �� ������� ������� ��� ���� ������, ������������ �� �������� (����� ���������).
- ������� ��� ������� � ���������� ����������.
- ��������� ��� ������ �� �������� ������ � �������.


## ������ ���������
������ ������� ������� ������� ����� ��������� ������.

��������� ���� ������ (system, INFORMATION_SCHEMA, information_schema) ������������.

������ ����������� ������� �� 100,000 ����� ��� �������������.