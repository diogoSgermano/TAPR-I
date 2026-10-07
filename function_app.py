import logging
import os

import azure.functions as func
import pyodbc


app = func.FunctionApp()


@app.timer_trigger(
    schedule="0 * * * * *",
    arg_name="myTimer",
    run_on_startup=False,
    use_monitor=False
)
def extract_db(myTimer: func.TimerRequest) -> None:

    # Dados de conexão
    host = os.getenv("HOST")
    database = os.getenv("DATABASE")
    user = os.getenv("USER")
    password = os.getenv("PASSWORD")

    # String de conexão
    conn_str = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={host};"
        f"DATABASE={database};"
        f"UID={user};"
        f"PWD={password};"
        "Encrypt=yes;"
        "TrustServerCertificate=yes;"
        "Connection Timeout=30;"
    )

    conn = None
    cursor = None

    try:
        logging.info("Iniciando execução da função extract_db.")

        logging.info(f"HOST: {host}")
        logging.info(f"DATABASE: {database}")
        logging.info(f"USER: {user}")

        # Conecta ao banco
        conn = pyodbc.connect(conn_str)
        logging.info("Conexão com o banco de dados estabelecida com sucesso.")

        # Cria o cursor
        cursor = conn.cursor()

        logging.info("Executando SELECT na tabela itsm.chamado")

        cursor.execute("""
            SELECT *
            FROM itsm.chamado
        """)

        # Recupera os registros
        registros = cursor.fetchall()

        logging.info(
            f"Total de registros encontrados: {len(registros)}"
        )

        # Exibe os registros
        for registro in registros:
            logging.info(f"Chamado: {registro}")

        logging.info("Consulta executada com sucesso.")

    except pyodbc.Error as e:
        logging.error(
            f"Erro de conexão ou consulta no SQL Server: {e}"
        )

    except Exception as e:
        logging.error(
            f"Erro inesperado durante a execução: {e}"
        )

    finally:
        # Fecha o cursor
        if cursor is not None:
            cursor.close()
            logging.info("Cursor encerrado.")

        # Fecha a conexão
        if conn is not None:
            conn.close()
            logging.info("Conexão com o banco encerrada.")

        logging.info("Execução da função extract_db finalizada.")