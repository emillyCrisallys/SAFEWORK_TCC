import psycopg2
import os
from dotenv import load_dotenv

load_dotenv() # Carrega as variáveis do .env

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
    query = """
    INSERT INTO public.deteccoes (
        id_camera, id_funcionario, tipo_falta_epi, 
        path_imagem_original, path_imagem_blur, 
        confianca_ia, tempo_processamento_ms
    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(query, (
            dados['id_camera'], dados.get('id_funcionario'), 
            dados['tipo_falta_epi'], dados['path_original'], 
            dados['path_blur'], dados['confianca'], 
            dados['tempo_ms']
        ))
        conn.commit()
    except Exception as e:
        print(f"Erro ao salvar detecção: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()