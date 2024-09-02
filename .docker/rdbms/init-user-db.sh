# init-user-db.sh
#!/bin/bash
set -e


# Read the APP_PASSWORD value from the file
if [ ! -f "$APP_PASSWORD_FILE" ]; then
    echo "Error: File APP_PASSWORD_FILE=$APP_PASSWORD_FILE does not exist."
    exit 1
fi

APP_PASSWORD=$(cat "$APP_PASSWORD_FILE")

# Check if the file is empty
if [ -z "$APP_PASSWORD" ]; then
    echo "Error: APP_PASSWORD value is empty."
    exit 1
fi


# Read the APP_USER value from the file
if [ ! -f "$APP_USER_FILE" ]; then
    echo "Error: File APP_USER_FILE=$APP_USER_FILE does not exist."
    exit 1
fi

APP_USER=$(cat "$APP_USER_FILE")

# Check if the file is empty
if [ -z "$APP_USER" ]; then
    echo "Error: APP_USER value is empty."
    exit 1
fi

# Read the APP_DB value from the file
if [ ! -f "$APP_DB_FILE" ]; then
    echo "Error: File APP_DB_FILE=$APP_DB_FILE does not exist."
    exit 1
fi

APP_DB=$(cat "$APP_DB_FILE")

# Check if the file is empty
if [ -z "$APP_DB" ]; then
    echo "Error: APP_DB value is empty."
    exit 1
fi

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER $APP_USER WITH PASSWORD '$APP_PASSWORD';
    CREATE DATABASE $APP_DB OWNER $APP_USER;
    GRANT ALL PRIVILEGES ON DATABASE $APP_DB TO $APP_USER;
EOSQL

# echo port = ${POSTGRES_PORT} > /etc/postgresql/postgresql.conf

