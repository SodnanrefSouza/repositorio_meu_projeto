from django.shortcuts import render
from django.db import connection
from django.contrib.auth.decorators import login_required

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
            # Consulta para listar as tabelas
            cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
            tables = cursor.fetchall()
            print("Tabelas encontradas:", tables)  # Debug: imprime as tabelas encontradas

            # Para cada tabela encontrada, consulte suas colunas
            for table in tables:
                table_name = table[0]
                cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}';")
                columns = cursor.fetchall()
                print(f"Colunas da tabela {table_name}:", columns)  # Debug: imprime as colunas da tabela
                table_columns[table_name] = [col[0] for col in columns]
    except Exception as e:
        print(f"Erro ao listar tabelas: {e}")

    return render(request, 'gerenciador_tabelas/list_tables.html', {'table_columns': table_columns})

