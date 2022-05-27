import csv
import unidecode
import openpyxl
import pandas as pd
import pyodbc
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

with open('_config\config_historico.csv', 'r') as arquivo_csv:
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
df_sql = pd.DataFrame()

def consulta_itens_excluidos(pedido, cliente):
        pedido = str(pedido)
        cliente = str(cliente)
        
        consulta = f"""
        SELECT 
        CD_PEDIDO, 
        CD_ITEM, 
        CD_MATERIAL, 
        DS_MATERIAL, 
        NR_QUANTIDADE, 
        VL_UNITARIO, 
        VL_TOTAL, 
        (VL_ICMS_SUBST + VL_FCP_ST) AS VL_ST, 
        (VL_TOTAL + (VL_ICMS_SUBST + VL_FCP_ST)) AS VL_TOTAL_COM_ST  
            FROM TBL_PEDIDOS_itens
                where cd_pedido = {pedido};
        """                   

        if pedido != "":
            pedido = f"AND T1.CD_PEDIDO IN (0,{pedido}) "
        else:
            pass
        if cliente != "":
            cliente = f"AND T2.CD_CLIENTE IN (0,{cliente})"
        else:
            pass

        consulta2 = f"""
        SELECT T2.CD_CLIENTE, 
        T3.DS_ENTIDADE, 
        T1.DT_CADASTRO, 
        T1.CD_PEDIDO, 
        CD_ITEM, 
        CD_MATERIAL, 
        DS_MATERIAL, 
        T1.NR_QUANTIDADE, 
        VL_UNITARIO, 
        T1.VL_TOTAL, 
        (T1.VL_ICMS_SUBST + T1.VL_FCP_ST) AS VL_ST, 
        (T1.VL_TOTAL + (T1.VL_ICMS_SUBST + T1.VL_FCP_ST)) AS VL_TOTAL_COM_ST   
            FROM nGestao_Historico_Dados.dbo.TBL_PEDIDOS_itens T1
                INNER JOIN nGestao.dbo.TBL_PEDIDOS T2
                    ON T1.CD_PEDIDO = T2.CD_PEDIDO
                INNER JOIN nGestao.dbo.TBL_ENTIDADES T3
                    ON T2.CD_CLIENTE = T3.CD_ENTIDADE
                    WHERE T1.DT_CADASTRO >= CONVERT(datetime, '2022-01-01T00:00:00.000')
                        {pedido}
                        {cliente}
                            ORDER BY T1.DT_CADASTRO DESC
                        ;
        
        """

        cursor.execute(consulta2)

        resultados = cursor.fetchall()

        num_colunas = len(cursor.description)
        nome_colunas = [i[0] for i in cursor.description]

        dados = (resultados, nome_colunas)
        return dados