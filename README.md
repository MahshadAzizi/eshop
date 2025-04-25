## Environment Variables
### 1. `.env` File
This file contains configuration for the Backend service, Celery, Redis, and Database connections.

#### Example `.env` File:
```ini
  SECRET_KEY=
  DEBUG=
  ALLOWED_HOSTS=
  DATABASE_NAME=
  DATABASE_USER=
  DATABASE_PASS=
  DATABASE_HOST=
  DATABASE_PORT=
  REDIS_HOST=
  REDIS_PORT=
  REDIS_DB=
  CELERY_BROKER_URL=
  CELERY_RESULT_BACKEND=
```
### 2. `db.env` File
This file contains configuration for the PostgreSQL database.

#### Example `db.env` File:
```ini
POSTGRES_DB=POSTGRES_DB
POSTGRES_USER=POSTGRES_USER
POSTGRES_PASSWORD=POSTGRES_PASSWORD
POSTGRES_HOST=POSTGRES_HOST
POSTGRES_PORT=POSTGRES_PORT
```

## How to run the app: 
1. Clone the repository:
 ```sh
 $ git clone https://github.com/MahshadAzizi/eshop.git
 $ cd eshop
 ```
2. Build and run the Docker containers:
 ```sh
  $ docker compose up -d --build
 ```
