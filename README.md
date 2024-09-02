# Auto Factra

This project is meant to be a backend service where you can upload receipts of your purchases and it would automatically create a tax declaration for that purchase.

# Set up

Built in python 3.12.3

Add the files:

 - .docker/rdbms/secrets/postgres-app-db
 - .docker/rdbms/secrets/postgres-app-passwd
 - .docker/rdbms/secrets/postgres-app-user
 - .docker/rdbms/secrets/postgres-default-db
 - .docker/rdbms/secrets/postgres-super-passwd
 - .docker/rdbms/secrets/postgres-superuser

These files must contain only one line wih the value for the db connection.

# How to use