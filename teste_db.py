from src.database import get_db_connection

try:
    conn = get_db_connection()
    cur = conn.cursor()
    # Testando se as tabelas que você criou existem
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
    tabelas = cur.fetchall()
    print("Conexão bem-sucedida! Tabelas encontradas:")
    for t in tabelas:
        print(f"- {t[0]}")
    cur.close()
    conn.close()
except Exception as e:
    print(f"Erro na conexão: {e}")