#!/usr/bin/env python3
import time
import os
import psycopg2

def wait_for_postgres():
    host = os.getenv('POSTGRES_HOST', 'database')
    port = int(os.getenv('POSTGRES_PORT', '5432'))
    user = os.getenv('POSTGRES_USER', 'pablodutra')
    password = os.getenv('POSTGRES_PASSWORD', '987@passDutra')
    dbname = os.getenv('POSTGRES_DB', 'bancodados')
    while True:
        try:
            conn = psycopg2.connect(host=host, port=port, user=user, password=password, dbname=dbname)
            conn.close()
            print('Postgres está pronto!')
            break
        except Exception as e:
            print(f'Aguardando Postgres... {e}')
            time.sleep(2)

if __name__ == '__main__':
    wait_for_postgres()
    os.system('uvicorn app.main:app --host 0.0.0.0 --port 8000')
