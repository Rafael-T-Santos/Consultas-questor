from os import close
import pyodbc
import pandas as pd
import openpyxl
import unidecode
import csv

with open('config.csv', 'r') as arquivo_csv:
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

user = 'WANESSA'
senha = '261200'


def consulta_usuario():
    consulta = """SELECT DS_LOGIN, DS_SENHA FROM TBL_USUARIOS"""
    df = pd.read_sql_query(consulta, cnxn)
    df = df.set_index('DS_LOGIN')

    print(df.index[df['DS_SENHA'] == senha].tolist())
    if user in df.index[df['DS_SENHA'] == senha]:
        print('Login Liberado!')
    else:
        print('Senha Incorreta')


consulta_usuario()
