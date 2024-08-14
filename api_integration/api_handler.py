import os
import pandas as pd
import requests
import json
from sqlalchemy import create_engine, text

class APIIntegration:
    def __init__(self, database_connection):
        self.database_connection = database_connection
        self.engine = create_engine(database_connection)

    def execute_query(self, query):
        with self.engine.connect() as connection:
            connection.execute(text(query))

    def table_ingestion(self, api_url, table_name, json_key, app_secret=None, headers=None):
        pagina = 0
        status = True

        while status:
            if app_secret:
                headers = headers or {}
                headers['Authorization'] = app_secret
            
            params = {"page": pagina}
            response = requests.get(api_url, headers=headers, params=params)
            
            if response.status_code == 200:
                data = response.json().get(json_key)
                if not data:  # Verifica se há dados para processar
                    break
                
                df = pd.json_normalize(data)
                # Substituir ou adicionar os dados à tabela do banco de dados
                if pagina == 0:
                    df.to_sql(table_name, con=self.engine, if_exists='replace', index=False)
                else:
                    df.to_sql(table_name, con=self.engine, if_exists='append', index=False)
                
                pagina += 1
            else:
                status = False  # Finaliza o loop se houver erro na requisição

        self.engine.dispose()

# Exemplo de uso
if __name__ == "__main__":
    database_connection = "postgresql://user:password@localhost/dbname"
    api_handler = APIIntegration(database_connection)

    # Ingestão de dados
    api_handler.table_ingestion(
        api_url='https://api.example.com/data',
        table_name='my_table',
        json_key='items'
    )
