import os
import pandas as pd
import requests
import json
import datetime
from django.shortcuts import render
from django.db import connection
from django.contrib.auth.decorators import login_required

# Configurações de conexão com a API
LIST_ID = "901304272771"
URL = f"https://api.clickup.com/api/v2/list/{LIST_ID}/task"
APP_SECRET = 'pk_81983449_DJ9QEMONLMZKYDZE1ZJV5MBJBC7M3UEP'

# Lista de arquivos de SQL
SQL_FILES = {
    "elimina_tabela": 'elimina_tabela_clickup_data_opportunities.sql',
    "cria_tabela": 'cria_tabela_clickup_data_opportunities.sql',
    "elimina_colunas": 'elimina_colunas_nao_utilizadas.sql',
    "adiciona_colunas": 'adiciona_colunas_ajuste_data.sql',
    "seta_valores": 'seta_valores_colunas_ajuste_data.sql',
    "elimina_ajuste": 'elimina_colunas_ajuste.sql',
    "renomeia_ajuste": 'renomeia_colunas_ajuste.sql'
}

OUTPUT_FILE = "./output.xlsx"
SHEET_NAME = 'Sheet1'


def flatten_json(data, prefix=''):
    """Achata um JSON, transformando listas e dicionários em um formato plano."""
    if isinstance(data, dict):
        new_data = {}
        for key, value in data.items():
            if isinstance(value, list):
                # Se for uma lista, itera sobre ela
                for i, item in enumerate(value):
                    new_data.update(flatten_json(item, prefix + key + str(i) + '_'))
            elif isinstance(value, dict):
                new_data.update(flatten_json(value, prefix + key + '_'))
            else:
                new_data[prefix + key] = value
        return new_data
    else:
        return {prefix: data}


def execute_sql_file(sql_file):
    """Executa um arquivo de SQL e trata exceções."""
    with open(sql_file, 'r') as file:
        query = file.read()
    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
            print(f"Query do arquivo {sql_file} executada com sucesso.")
        except Exception as e:
            print(f"Erro ao tentar executar query do arquivo {sql_file}: {e}.")


def ingest_data(url, table_name, json_key, app_secret):
    """Injeta dados da API ClickUp no banco de dados."""
    # Executa as queries de criação e limpeza
    execute_sql_file(SQL_FILES["elimina_tabela"])
    execute_sql_file(SQL_FILES["cria_tabela"])

    page = 0
    while True:
        params = {"include_closed": "true", "page": str(page)}
        headers = {"Authorization": app_secret}

        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            print("Erro ao obter dados da API.")
            break

        tasks = response.json().get(json_key)
        if not tasks:
            print("Nenhuma tarefa encontrada.")
            break

        flat_data = [flatten_json(task) for task in tasks]
        df = pd.json_normalize(flat_data)

        # Salva em Excel como intermediário
        df.to_excel(OUTPUT_FILE, index=False)

        # Lê o Excel e insere no banco de dados
        with connection.cursor() as cursor:
            for index, row in df.iterrows():
                # Cria a inserção dinâmica (ajuste conforme seu modelo de tabela)
                sql_insert = f"INSERT INTO {table_name} ({', '.join(row.index)}) VALUES ({', '.join(['%s'] * len(row))})"
                cursor.execute(sql_insert, tuple(row))

        page += 1
        if page >= response.json().get("last_page", 0):
            break

    # Executa as queries para ajuste dos dados
    for action in ["elimina_colunas", "adiciona_colunas", "seta_valores", "elimina_ajuste", "renomeia_ajuste"]:
        execute_sql_file(SQL_FILES[action])

    # Remove o arquivo auxiliar
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)


def log_execution(start_time):
    """Registra informações sobre a execução."""
    end_time = datetime.datetime.now()
    duration = end_time - start_time
    with open("log.txt", "a") as log_file:
        log_file.write(f"{start_time} - Horário de Início\n")
        log_file.write(f"{end_time} - Tempo de execução: {duration}\n")


@login_required
def run_data_ingestion(request):
    """Função que chama a ingestão de dados a partir da API."""
    start_time = datetime.datetime.now()
    log_execution(start_time)

    # Ingesta os dados da ClickUp
    ingest_data(URL, 'clickup_data_opportunities', "tasks", APP_SECRET)

    # Atualiza o tempo de execução no log
    log_execution(datetime.datetime.now())
    
    return render(request, 'success.html')  # Redireciona para uma página de sucesso


if __name__ == "__main__":
    run_data_ingestion()  # Essa linha é apenas para testes fora do Django
