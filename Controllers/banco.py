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


def consulta_produtos(produtos):
    
    consulta = """
    SELECT 
    T1.CD_MATERIAL AS 'CÓD.', 
    T3.DS_MATERIAL AS 'DESCRIÇÃO', 
    (SELECT NR_ESTOQUE_DISPONIVEL FROM TBL_MATERIAIS_ESTOQUE T2 WHERE T1.CD_MATERIAL=T2.CD_MATERIAL AND CD_FILIAL=1) AS 'Filial-1', 
    (SELECT NR_ESTOQUE_DISPONIVEL FROM TBL_MATERIAIS_ESTOQUE T2 WHERE T1.CD_MATERIAL=T2.CD_MATERIAL AND CD_FILIAL=2) AS 'Filial-2', 
    (SELECT NR_ESTOQUE_DISPONIVEL FROM TBL_MATERIAIS_ESTOQUE T2 WHERE T1.CD_MATERIAL=T2.CD_MATERIAL AND CD_FILIAL=3) AS 'Filial-3', 
    (SELECT NR_ESTOQUE_DISPONIVEL FROM TBL_MATERIAIS_ESTOQUE T2 WHERE T1.CD_MATERIAL=T2.CD_MATERIAL AND CD_FILIAL=4) AS 'Filial-4', 
    (SELECT NR_ESTOQUE_DISPONIVEL FROM TBL_MATERIAIS_ESTOQUE T2 WHERE T1.CD_MATERIAL=T2.CD_MATERIAL AND CD_FILIAL=5) AS 'Filial-5', 
    (SELECT NR_ESTOQUE_DISPONIVEL FROM TBL_MATERIAIS_ESTOQUE T2 WHERE T1.CD_MATERIAL=T2.CD_MATERIAL AND CD_FILIAL=6) AS 'Filial-6' 
        FROM TBL_MATERIAIS_ESTOQUE T1
            INNER JOIN TBL_MATERIAIS T3 ON T1.CD_MATERIAL = T3.CD_MATERIAL
                WHERE T1.CD_MATERIAL IN("""+produtos+""")
                    GROUP BY T1.CD_MATERIAL, T3.DS_MATERIAL;
                """

    # armazena as informações sobre a consulta, numero de colunas, nomes, tipos de dados
    cursor.execute(consulta)
    # armazena os dados
    resultados = cursor.fetchall()
    # pega o tamanho da descrição do cursor, ou seja o numero de colunas
    num_colunas = len(cursor.description)
    nome_colunas = [i[0] for i in cursor.description]

    dados = (resultados, nome_colunas)
    return dados

def consulta_fecoep():

        consulta = """
        SELECT  
        T2.CD_MATERIAL AS COD, 
		T2.DS_MATERIAL AS DESCRICAO, 
		T1.CD_UF AS UF,
		T1.PR_FCP_MATERIAL AS FECOEP, 
		T2.CD_GRADE_TRIBUTARIA AS CD_GRADE, 
		T3.DS_GRADE AS GRADE, 
		T2.CD_FILIAL_MATERIAL AS FILIAL, 
		(CASE WHEN T2.X_CALCULA_FCP = 1
			THEN 'SIM' ELSE 'NÃO' END) AS CALC_FCP, 
		(CASE WHEN T2.X_CALCULA_FCP_ST = 1 
			THEN 'SIM' ELSE 'NÃO' END) AS CALC_FCP_ST
			FROM TBL_MATERIAIS_ALIQUOTA_UF_DIFAL_FCP T1
				RIGHT JOIN TBL_MATERIAIS T2 ON T1.CD_MATERIAL = T2.CD_MATERIAL
				INNER JOIN TBL_GRADE_TRIBUTARIA T3 ON T2.CD_GRADE_TRIBUTARIA = T3.CD_GRADE
					WHERE T2.CD_GRADE_TRIBUTARIA NOT IN (33,37,38)
                    AND T1.PR_FCP_MATERIAL IS NULL
					UNION 
						SELECT  T2.CD_MATERIAL AS COD, 
								T2.DS_MATERIAL AS DESCRICAO, 
								T1.CD_UF AS UF,
								T1.PR_FCP_MATERIAL AS FECOEP, 
								T2.CD_GRADE_TRIBUTARIA AS CD_GRADE, 
								T3.DS_GRADE AS GRADE, 
								T2.CD_FILIAL_MATERIAL AS FILIAL, 
								(CASE WHEN T2.X_CALCULA_FCP = 1 
									THEN 'SIM' ELSE 'NÃO' END) AS CALC_FCP, 
								(CASE WHEN T2.X_CALCULA_FCP_ST = 1 
									THEN 'SIM' ELSE 'NÃO' END) AS CALC_FCP_ST
									FROM TBL_MATERIAIS_ALIQUOTA_UF_DIFAL_FCP T1
										RIGHT JOIN TBL_MATERIAIS T2 ON T1.CD_MATERIAL = T2.CD_MATERIAL
										INNER JOIN TBL_GRADE_TRIBUTARIA T3 ON T2.CD_GRADE_TRIBUTARIA = T3.CD_GRADE
											WHERE T2.CD_GRADE_TRIBUTARIA NOT IN (33,37,38)
											AND T2.X_CALCULA_FCP = 0
											UNION
												SELECT  T2.CD_MATERIAL AS COD, 
														T2.DS_MATERIAL AS DESCRICAO, 
														T1.CD_UF AS UF,
														T1.PR_FCP_MATERIAL AS FECOEP, 
														T2.CD_GRADE_TRIBUTARIA AS CD_GRADE, 
														T3.DS_GRADE AS GRADE, 
														T2.CD_FILIAL_MATERIAL AS FILIAL, 
														(CASE WHEN T2.X_CALCULA_FCP = 1 
															THEN 'SIM' ELSE 'NÃO' END) AS CALC_FCP, 
														(CASE WHEN T2.X_CALCULA_FCP_ST = 1 
															THEN 'SIM' ELSE 'NÃO' END) AS CALC_FCP_ST
														FROM TBL_MATERIAIS_ALIQUOTA_UF_DIFAL_FCP T1
															RIGHT JOIN TBL_MATERIAIS T2 ON T1.CD_MATERIAL = T2.CD_MATERIAL
															INNER JOIN TBL_GRADE_TRIBUTARIA T3 ON T2.CD_GRADE_TRIBUTARIA = T3.CD_GRADE
																WHERE T2.CD_GRADE_TRIBUTARIA NOT IN (33,37,38,3)
																AND T2.X_CALCULA_FCP_ST = 0;
                    """
        
        cursor.execute(consulta)

        resultados = cursor.fetchall()

        num_colunas = len(cursor.description)
        nome_colunas = [i[0] for i in cursor.description]

        dados = (resultados, nome_colunas)
        return dados

def faturamento_cpf():

        consulta = """
        SELECT DISTINCT 
        T1.CD_LANCAMENTO, 
        T1.NR_DOCUMENTO, 
        T1.CD_CLIENTE, 
        T2.DS_ENTIDADE,
        T2.NR_CPFCNPJ,
        T1.DT_EMISSAO 
            FROM TBL_NOTAS_FATURAMENTO T1
                INNER JOIN TBL_ENTIDADES T2 ON T1.CD_CLIENTE = T2.CD_ENTIDADE
                    WHERE T1.CD_FILIAL = 1
                    AND T1.CD_STATUS_NFE_RETORNO = 100
                    AND LEN(T2.NR_CPFCNPJ) < 18
                    AND (T1.DT_EMISSAO > CONVERT(datetime, '2022-01-01T00:00:00.000'))
                        ORDER BY T1.DT_EMISSAO DESC;
                    """

        cursor.execute(consulta)

        resultados = cursor.fetchall()

        num_colunas = len(cursor.description)
        nome_colunas = [i[0] for i in cursor.description]

        dados = (resultados, nome_colunas)
        return dados

def consulta_personalizada(sql_personalizado):
      
        cursor.execute(sql_personalizado)

        resultados = cursor.fetchall()

        num_colunas = len(cursor.description)
        nome_colunas = [i[0] for i in cursor.description]

        dados = (resultados, nome_colunas)
        return dados

def consulta_faturadas_email(data):
        
        consulta = """
        SELECT DISTINCT 
        T2.CD_ENTIDADE, 
        T2.DS_EMAIL 
            FROM TBL_NOTAS_FATURAMENTO T1
                INNER JOIN TBL_ENTIDADES T2 ON T1.CD_CLIENTE = T2.CD_ENTIDADE
                    WHERE T1.CD_FILIAL = 1
                    AND (T1.DT_EMISSAO = CONVERT(datetime, '"""+data+"""T00:00:00.000'))
                    AND T1.CD_STATUS_NFE_RETORNO = 100
                    AND T2.DS_EMAIL <> ''
                        ORDER BY T2.CD_ENTIDADE;
                    """


        cursor.execute(consulta)

        resultados = cursor.fetchall()

        num_colunas = len(cursor.description)
        nome_colunas = [i[0] for i in cursor.description]

        dados = (resultados, nome_colunas)
        return dados

def consulta_retiradas():

        consulta = """
        SELECT 
        T3.NR_DOCUMENTO, 
        T1.CD_ITEM AS ITEM, 
        T1.CD_MATERIAL AS COD, 
        T1.DS_MATERIAL AS PRODUTO, 
        T1.CD_CME AS COD, 
        T1.DS_CME AS NATUREZA, 
        T1.NR_QUANTIDADE AS QUANTIDADE,
        (CASE WHEN (T1.NR_QUANTIDADE - (SELECT SUM(NR_QUANTIDADE) 
                                            FROM SEL_NOTAS_EMITIDAS_ITENS T2 
                                                WHERE T1.CD_MATERIAL = T2.CD_MATERIAL
                                                AND T1.CD_LANCAMENTO = T2.CD_NOTA_FATURAMENTO_IMPORTADA
                                                    GROUP BY T2.CD_MATERIAL)) IS NULL THEN 0 
                                                        ELSE 
                                                            (T1.NR_QUANTIDADE - (SELECT SUM(NR_QUANTIDADE) 
                                                                                    FROM SEL_NOTAS_EMITIDAS_ITENS T2 
                                                                                        WHERE T1.CD_MATERIAL = T2.CD_MATERIAL
                                                                                        AND T1.CD_LANCAMENTO = T2.CD_NOTA_FATURAMENTO_IMPORTADA
                                                                                            GROUP BY T2.CD_MATERIAL)) END) AS QUANT_IMPORTAR,  
        (CASE WHEN (SELECT SUM(NR_QUANTIDADE) 
                        FROM SEL_NOTAS_EMITIDAS_ITENS T2
                            WHERE T1.CD_MATERIAL = T2.CD_MATERIAL
                            AND T1.CD_LANCAMENTO = T2.CD_NOTA_FATURAMENTO_IMPORTADA
                                GROUP BY T2.CD_MATERIAL) IS NULL THEN 0 
                                    ELSE 
                                        (SELECT SUM(NR_QUANTIDADE) 
                                            FROM SEL_NOTAS_EMITIDAS_ITENS T2 
                                                WHERE T1.CD_MATERIAL = T2.CD_MATERIAL
                                                AND T1.CD_LANCAMENTO = T2.CD_NOTA_FATURAMENTO_IMPORTADA
                                                    GROUP BY T2.CD_MATERIAL) END) AS QUANT_FATURADA
            FROM DBO.TBL_NOTAS_FATURAMENTO_ITENS T1
                INNER JOIN TBL_NOTAS_FATURAMENTO T3
                ON T1.CD_LANCAMENTO = T3.CD_LANCAMENTO
                    WHERE (X_SIMPLES_REMESSA_ENTREGA_FUTURA = 1)
                    AND T1.NR_QUANTIDADE <> (SELECT SUM(NR_QUANTIDADE) 
                                                FROM SEL_NOTAS_EMITIDAS_ITENS T2 
                                                    WHERE T1.CD_MATERIAL = T2.CD_MATERIAL
                                                    AND T1.CD_LANCAMENTO = T2.CD_NOTA_FATURAMENTO_IMPORTADA
                                                        GROUP BY T2.CD_MATERIAL)
                                                            ORDER BY NR_DOCUMENTO DESC;
                    """


        cursor.execute(consulta)

        resultados = cursor.fetchall()

        num_colunas = len(cursor.description)
        nome_colunas = [i[0] for i in cursor.description]

        dados = (resultados, nome_colunas)
        return dados