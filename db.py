import os
import pyodbc

def get_conn():
    return pyodbc.connect(os.environ["SQL_CONN_STR"])
