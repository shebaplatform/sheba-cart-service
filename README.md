# Setup PostgreSql
```
docker run --name postgres-db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=cart_db \
  -p 5432:5432 \
  -v pgdata:/var/lib/postgresql/data \
  -d postgres:17.4
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