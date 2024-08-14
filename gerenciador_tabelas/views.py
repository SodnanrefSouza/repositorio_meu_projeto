from django.shortcuts import render
from django.db import connection
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

@login_required
def create_table(request):
    if request.method == 'POST':
        table_name = request.POST.get('table_name')
        column_definitions = request.POST.get('column_definitions')
        
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE TABLE {table_name} ({column_definitions});")
        
        # Renderiza a página de confirmação com o nome da tabela
        return render(request, 'gerenciador_tabelas/table_created.html', {'table_name': table_name})
    
    return render(request, 'gerenciador_tabelas/create_table.html')

@login_required
def list_tables(request):
    table_columns = {}
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT c.table_name, c.column_name, c.data_type, d.description
                FROM information_schema.columns AS c
                LEFT JOIN pg_catalog.pg_description AS d ON d.objoid = c.table_name::regclass AND d.objsubid = c.ordinal_position
                WHERE c.table_schema='public'
                ORDER BY c.table_name, c.ordinal_position;
            """)
            columns_info = cursor.fetchall()

            # Organiza as informações em um dicionário
            for table_name, column_name, data_type, description in columns_info:
                if table_name not in table_columns:
                    table_columns[table_name] = []
                table_columns[table_name].append({
                    'column_name': column_name,
                    'type': data_type,
                    'description': description or 'Sem descrição'  # Caso não haja descrição, pode-se usar um valor padrão
                })

    except Exception as e:
        print(f"Erro ao listar tabelas: {e}")

    # Paginação
    paginator = Paginator(list(table_columns.items()), 5)  # 5 tabelas por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'gerenciador_tabelas/list_tables.html', {'page_obj': page_obj})

@login_required
def list_table_records(request, table_name):
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]

        # Paginação
        paginator = Paginator(rows, 10)  # Mostra 10 registros por página
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    except Exception as e:
        print(f"Erro ao listar registros da tabela {table_name}: {e}")
        return render(request, 'gerenciador_tabelas/list_table_records.html', {'error': str(e), 'table_name': table_name})

    return render(request, 'gerenciador_tabelas/list_table_records.html', {
        'table_name': table_name,
        'page_obj': page_obj,
        'column_names': column_names
    })

