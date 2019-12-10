cd db

find . -name "*.db" -type f -delete

sqlite3 amazon.db < ./sql/populate-amazon.sql;

find . -name "*.db" -type f