import psycopg2
import os
from dotenv import load_dotenv

load_dotenv() 

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        port=os.getenv("DB_PORT")
    )
    return conn

def salvar_deteccao(dados):
    # 1. Conexão com suporte a UTF-8
    conn = get_db_connection()
    # Forçar a conexão a tratar tudo como UTF-8
    conn.set_client_encoding('UTF8')
    cur = conn.cursor()
    
    try:
        # 2. Se o dado do funcionário for um nome (string), buscamos o ID
        id_func = dados.get('id_funcionario')
        nome = dados.get('funcionario') # Nome vindo do detector.py
        
        if id_func is None and nome and nome != "Desconhecido":
            cur.execute("SELECT id_funcionario FROM public.funcionarios WHERE nome = %s", (nome,))
            res = cur.fetchone()
            if res:
                id_func = res[0]
        
        # 3. Execução do INSERT
        query = """
        INSERT INTO public.deteccoes (
            id_camera, id_funcionario, tipo_falta_epi, 
            path_imagem_original, path_imagem_blur, 
            confianca_ia, tempo_processamento_ms
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        cur.execute(query, (
            dados.get('id_camera', 1), # Default 1 se não vier
            id_func, 
            dados.get('tipo'), 
            dados.get('path_original'), 
            dados.get('path_blur', ''), # Caso blur não exista ainda
            dados.get('confianca'), 
            dados.get('tempo_ms', 0)
        ))
        conn.commit()
        print("Detecção salva com sucesso no banco!")
        
    except Exception as e:
        print(f"Erro ao salvar detecção: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()