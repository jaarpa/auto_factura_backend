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


psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER $APP_USER WITH PASSWORD '$APP_PASSWORD';
    CREATE DATABASE $APP_DB OWNER $APP_USER;
    GRANT ALL PRIVILEGES ON DATABASE $APP_DB TO $APP_USER;
EOSQL
