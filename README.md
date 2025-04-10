# Setup PostgreSql

### Docker run
```
docker run --name postgres-db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=cart_db \
  -p 5432:5432 \
  -v pgdata:/var/lib/postgresql/data \
  -d postgres:17.4
```

### Create database and user
```
docker exec -it postgresql bash
psql -U postgres
CREATE USER sheba_user WITH PASSWORD 'your_secure_password';
CREATE DATABASE sheba_cart_db OWNER sheba_user;
GRANT ALL PRIVILEGES ON DATABASE sheba_cart_db TO sheba_user;
GRANT ALL ON SCHEMA public TO sheba_user;
```

# Setup virtual environment

### Step 1: Create the virtual environment
``` 
python3 -m venv venv
```

### Activate the virtual environment
``` 
source venv/bin/activate
```

### Install python libraries
```
pip3 install -r requirements.txt
```

# Alembic Migration Setup

### Install Alembic
```
pip install alembic
```

### Initialize Alembic
```
alembic init alembic
```

### Generate & Run Migration
```
alembic revision --autogenerate -m "initial tables"
alembic upgrade head
```

# Project Run

```
docker build -t cart_service .

docker run -itd -p 8000:8000 --name cart_service -v $(pwd):/app -w /app cart_service

```