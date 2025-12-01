import os
import pyodbc

def get_conn():
    return pyodbc.connect(os.environ["SQLCONNSTR_SQL_CONN_STR"])
