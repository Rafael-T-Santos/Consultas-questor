from os import close
import csv
import unidecode
import openpyxl
import pandas as pd
import pyodbc
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

with open('_config\config.csv', 'r') as arquivo_csv:
    leitor = csv.DictReader(arquivo_csv, delimiter=';')
    for coluna in leitor:
        server = coluna['server']
        database = coluna['database']
        username = coluna['username']
        password = coluna['password']

cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' +
                      server+';DATABASE='+database+';UID='+username+';PWD=' + password)
cursor = cnxn.cursor()
df = pd.DataFrame()
consulta = """SELECT DS_LOGIN, DS_SENHA FROM TBL_USUARIOS"""
df = pd.read_sql_query(consulta, cnxn)
df = df.set_index('DS_LOGIN')

def validar_usuario(login, senha):
    if login in df.index[df['DS_SENHA'] == senha]:
        return True
    else:
        return False
