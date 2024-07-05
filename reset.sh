#!/bin/bash

DB_PATH="app/db"

echo "On delete la db"
rm -f "${DB_PATH}/epicerie.db"

echo "On creer les tables"
sqlite3 "${DB_PATH}/epicerie.db" < "${DB_PATH}/db.sql"

echo "On insere les donnees..."
sqlite3 "${DB_PATH}/epicerie.db" < "${DB_PATH}/donnees_fictives.sql"

echo "Done!"
