#GUILHERME GOMES SOUZA
#DRE 11203916795


### QUESTÃO 1 ###

#BAIXAR ARQUIVOS 
from sqlite3.dbapi2 import Cursor
import requests
import os.path
import os

NOME_ARQUIVO_ENADE_2017 = "microdadosEnade2017.zip"
NOME_ARQUIVO_ENADE_2018 = "microdadosEnade2018.zip"
NOME_ARQUIVO_ENADE_2019 = "microdadosEnade2019.zip"

URL_ENADE_2019 = 'https://download.inep.gov.br/microdados/Enade_Microdados/microdados_enade_2019.zip'
URL_ENADE_2018 = 'https://download.inep.gov.br/microdados/Enade_Microdados/microdados_enade_2018.zip'
URL_ENADE_2017 = 'https://download.inep.gov.br/microdados/Enade_Microdados/microdados_Enade_2017_portal_2018.10.09.zip'

def baixar_arquivo(url, endereco):
    if not (os.path.isfile(endereco)):
        resposta = requests.get(url)
        if resposta.status_code == requests.codes.OK:
            with open(endereco, 'wb') as novo_arquivo:
                novo_arquivo.write(resposta.content)
            print ("Download finalizado. Salvo em %s" %(endereco))
        else: 
            resposta.raise_for_status()
    else:
        print("Arquivo %s já existe na pasta" %(endereco))

def baixa_todos_os_arquivos():
    baixar_arquivo(URL_ENADE_2019 , NOME_ARQUIVO_ENADE_2019)
    baixar_arquivo(URL_ENADE_2018 , NOME_ARQUIVO_ENADE_2018)
    baixar_arquivo(URL_ENADE_2017 , NOME_ARQUIVO_ENADE_2017)

#DESCOMPACTAR ARQUIVOS

import zipfile
from pathlib import Path

PASTA_ENADE_2019 = 'Enade2019'
PASTA_ENADE_2018 = 'Enade2018'
PASTA_ENADE_2017 = 'Enade2017'

def extrai_arquivo_zip(endereco, local):
    if not (os.path.isfile(local)):
        os.makedirs(local, exist_ok=True)
        with zipfile.ZipFile(endereco, 'r') as zip_ref:
            zip_ref.extractall(local)

def extrai_todos_os_arquivos():
    extrai_arquivo_zip(NOME_ARQUIVO_ENADE_2019, PASTA_ENADE_2019)
    extrai_arquivo_zip(NOME_ARQUIVO_ENADE_2018, PASTA_ENADE_2018)
    extrai_arquivo_zip(NOME_ARQUIVO_ENADE_2017, PASTA_ENADE_2017)


###QUESTÃO 3###
 
#CRIAR O BANCO DE DADOS
import sqlite3
NOME_BANCO = 'DW-ENADE.db'

def cria_banco(nome):
    banco = sqlite3.connect(nome)
    return banco


###QUESTÃO 4###
#CARREGAR ARQUIVOS NO PANDAS
import pandas as pd

CAMINHO_DADOS_2017_TXT = PASTA_ENADE_2017 + '/3.DADOS/MICRODADOS_ENADE_2017.txt'
CAMINHO_DADOS_2018_TXT = PASTA_ENADE_2018 + '/2018/3.DADOS/microdados_enade_2018.txt'
CAMINHO_DADOS_2019_TXT = PASTA_ENADE_2019 + '/3.DADOS/microdados_enade_2019.txt'

CAMINHO_DADOS_2017_CSV = PASTA_ENADE_2017 + '/3.DADOS/MICRODADOS_ENADE_2017.csv'
CAMINHO_DADOS_2018_CSV = PASTA_ENADE_2018 + '/2018/3.DADOS/microdados_enade_2018.csv'
CAMINHO_DADOS_2019_CSV = PASTA_ENADE_2019 + '/3.DADOS/microdados_enade_2019.csv'

def converte_txt_csv(caminho_origem, caminho_destino):
    if not (os.path.isfile(caminho_destino)):
        ler_arquivo = pd.read_csv(caminho_origem, sep = ";", skip_blank_lines=True)
        ler_arquivo.dropna(inplace = True)
        ler_arquivo.to_csv(caminho_destino, index = None)
    else:
        print("Arquivo já convertido anteriormente")

def converte_todos_txt_csv():
    converte_txt_csv(CAMINHO_DADOS_2017_TXT, CAMINHO_DADOS_2017_CSV)
    print("Arquivo 2017 convertido para csv")
    converte_txt_csv(CAMINHO_DADOS_2018_TXT, CAMINHO_DADOS_2018_CSV)
    print("Arquivo 2018 convertido para csv")
    converte_txt_csv(CAMINHO_DADOS_2019_TXT, CAMINHO_DADOS_2019_CSV)
    print("Arquivo 2019 convertido para csv")


def joga_dados_pandas(caminho):
    return pd.read_csv(caminho)

def joga_todos_dados_pandas():
    dados2017 = joga_dados_pandas(CAMINHO_DADOS_2017_CSV)
    dados2018 = joga_dados_pandas(CAMINHO_DADOS_2018_CSV)
    dados2019 = joga_dados_pandas(CAMINHO_DADOS_2019_CSV)
    return dados2017, dados2018, dados2019

def concat_anos(lista_dados_anos):
    return pd.concat(lista_dados_anos, join= "inner")

#CARGA DE DADOS NO BANCO

#DICIONÁRIOS COM VALORES DOS CÓDIGOS
DIC_ORGACAD = {"10019":"Centro Federal de Educação Tecnológica","10020" : "Centro Universitário", "10022": "Faculdade", "10026":"Instituto Federal de Educação, Ciência e Tecnologia", "10028": "Universidade"}
DIC_CATEGAD = {1: "Pública Federal", 2:"Pública Municipal",3: "Privada com fins lucrativos",4: "Privada sem fins lucrativos", 5: "Especial"}
DIC_GRUPO ={21: "Arquitetura e Urbanismo",72: "Tecnologia em Análise e Desenvolvimento de Sistemas",76: "Tecnologia em Gestão da Produção Industrial",79 : "Tecnologia em Redes de Computadores",701 : "Matemática (Bacharelado)",702 : "Matemática (Licenciatura)",903 : "Letras-Português (Bacharelado)",904 : "Letras-Português (Licenciatura)",905: "Letras-Português e Inglês (Licenciatura)",906: "Letras-Português e Espanhol (Licenciatura)",1401 : "Física (Bacharelado)",1402 : "Física (Licenciatura)",1501 : "Química (Bacharelado)",1502 : "Química (Licenciatura)",1601 : "Ciências Biológicas (Bacharelado)",1602 : "Ciências Biológicas (Licenciatura)",2001 : "Pedagogia (Licenciatura)",2401 : "História (Bacharelado)",2402 : "História (Licenciatura)",2501 : "Artes Visuais (Licenciatura)",3001 : "Geografia (Bacharelado)",3002 : "Geografia (Licenciatura)",3201 : "Filosofia (Bacharelado)",3202 : "Filosofia (Licenciatura)",3502 : "Educação Física (Licenciatura)}",4003 : "Engenharia Da Computação",4004 : "Ciência Da Computação (Bacharelado)",4005 : "Ciência Da Computação (Licenciatura)",4006 : "Sistemas De Informação",4301 : "Música (Licenciatura)",5401 : "Ciências Sociais (Bacharelado)",5402 : "Ciências Sociais (Licenciatura)",5710 : "Engenharia Civil",5806 : "Engenharia Elétrica",5814 : "Engenharia de Controle e Automação",5902 : "Engenharia Mecânica",6002 : "Engenharia de Alimentos",6008 : "Engenharia Química",6208 : "Engenharia de Produção",6306 : "Engenharia",6307 : "Engenharia Ambiental",6405 : "Engenharia Florestal",6407 : "Letras - Inglês",6409 : "Tecnologia em Gestão da Tecnologia da Informação"}
DIC_UF = {'11' : 'Rondônia (RO)','28' : 'Sergipe (SE)','12' : 'Acre (AC)','29' : 'Bahia (BA)', '13' : 'Amazonas (AM)', '31' : 'Minas gerais (MG)', '14' : 'Roraima (RR)','32' : 'Espírito santo (ES)',
          '15' : 'Para(PA)','33' : 'Rio de janeiro (RJ)','16' : 'Amapa (AP)','35' : 'São paulo (SP)','17' : 'Tocantins (TO)','41' : 'Paraná (PR)','21' : 'Maranhão (MA)','42' : 'Santa catarina (SC)',
          '22' : 'Piauí (PI)','43' : 'Rio grande do sul (RS)','23' : 'Ceará (CE)', '50' : 'Mato grosso do sul (MS)', '24' : 'Rio Grande do Norte (RN)','51' : 'Mato grosso (MT)', 
          '25' : 'Paraíba (PB)','52' : 'Goiás (GO)','26' : 'Pernambuco (PE)','53' : 'Distrito federal (DF)','27' : 'Alagoas (AL)'}
DIC_TURNO_GRADUACAO = ['','Matutino', 'Vespertino', 'Integral', 'Noturno']


def carrega_banco(banco, dados_enade):
    bd_abastece_curso(banco, dados_enade)
    bd_abastece_estudante(banco, dados_enade)
    bd_abastece_prova(banco, dados_enade)

def bd_abastece_prova(banco, dados_enade):
    cursor = banco.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS prova (NT_GER INT, NT_FG INT, NT_CE INT, INDEX_ALUNO INT, CO_CURSO INT, FOREIGN KEY(INDEX_ALUNO) REFERENCES estudante("index"), FOREIGN KEY(CO_CURSO) REFERENCES curso(CO_CURSO))')    
    dados_enade[["NT_GER", "NT_FG", "NT_CE"]].to_sql("prova", banco, if_exists = 'append', index = False)

def bd_abastece_estudante(banco, dados_enade):
    cursor = banco.cursor()
    # cursor.execute('CREATE TABLE IF NOT EXISTS estudante (NU_IDADE INT , TP_SEXO VARCHAR(1), ANO_FIM_EM VARCHAR(4), ANO_IN_GRAD VARCHAR(4), CO_TURNO_GRADUACAO VARCHAR(1), TP_INSCRICAO_ADM VARCHAR(1), TP_INSCRICAO VARCHAR(1))')
    dados_enade[["NU_IDADE", "TP_SEXO", "ANO_FIM_EM", "ANO_IN_GRAD", "CO_TURNO_GRADUACAO", "TP_INSCRICAO_ADM", "TP_INSCRICAO"]].to_sql("estudante" ,banco, if_exists='append')

def bd_abastece_curso(banco, dados_enade):
    cursor = banco.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS curso (CO_IES INT , CO_CATEGAD INT,CO_ORGACAD INT, CO_GRUPO INT, CO_CURSO INT, CO_MODALIDADE INT, CO_MUNIC_CURSO INT, CO_UF_CURSO INT, CO_REGIAO_CURSO INT, PRIMARY KEY(CO_CURSO))')
    dados_enade[["CO_IES", "CO_CATEGAD", "CO_ORGACAD", "CO_GRUPO", "CO_CURSO", "CO_MODALIDADE", "CO_MUNIC_CURSO", "CO_UF_CURSO", "CO_REGIAO_CURSO"]].to_sql("curso" ,banco, if_exists='append', index = False)
    

def filtra_dados_irreais(dados_enade):
    dados_enade_filtrados = dados_enade[(dados_enade.NU_IDADE > 10 )& (dados_enade.ANO_FIM_EM > 1957) &(dados_enade.ANO_FIM_EM < 2021)]    
    return dados_enade_filtrados

def remove_duplicatas_curso(dados_enade):
    return dados_enade.drop_duplicates(subset = ['CO_CURSO'], keep = 'first')


###QUESTÃO 5###
import matplotlib.pyplot as plot

def filtra_categorias(dados_enade):
    dados_enade_filtrados = dados_enade[(dados_enade.CO_CATEGAD < 6)]
    return dados_enade_filtrados

def filtra_grupos(dados_enade):
    dados_enade_filtrados = dados_enade[dados_enade['CO_GRUPO'].isin(DIC_GRUPO.keys())]
    return dados_enade_filtrados

#GENERO X NOTA
def relacao_genero_nota(dados_enade):
    dados_enade[["NT_GER"]] = dados_enade[["NT_GER"]].apply(lambda x: x.str.replace(',','.')).astype(float)
    print(dados_enade[["NT_GER", "TP_SEXO"]].groupby("TP_SEXO").mean())
    dados_enade[["NT_GER", "TP_SEXO"]].groupby("TP_SEXO").mean().plot.bar(rot = 70, title = "Relação Gênero x Nota Geral")
    plot.show()

#TIPO DE INSTITUICAO X NOTA
def relacao_instituicao_nota(dados_enade):
    dados_enade[["NT_GER"]] = dados_enade[["NT_GER"]].apply(lambda x: x.str.replace(',','.')).astype(float)
    dados_enade = dados_enade.replace(to_replace = DIC_CATEGAD, value= None)
    print(dados_enade[["NT_GER", "CO_CATEGAD"]].groupby("CO_CATEGAD").mean())
    dados_enade[["NT_GER", "CO_CATEGAD"]].groupby("CO_CATEGAD").mean().plot.bar(rot = 70, title = "Relação Tipo de Instituição x Nota Geral")
    plot.show()

#TIPO DE CURSO X NOTA
def relacao_curso_nota(dados_enade):
    dados_enade[["NT_GER"]] = dados_enade[["NT_GER"]].apply(lambda x: x.str.replace(',','.')).astype(float)
    # dados_enade = dados_enade.replace(to_replace = DIC_GRUPO)
    print(dados_enade[["NT_GER", "CO_GRUPO"]].groupby("CO_GRUPO").mean())
    dados_enade[["NT_GER", "CO_GRUPO"]].groupby("CO_GRUPO").mean().plot.bar(rot = 70, title = "Relação Grupo Curso x Nota Geral")
    plot.show()

####DEIXAR NO FINAL - RODA O PROGRAMA#####
if __name__ == "__main__":
    baixa_todos_os_arquivos()
    extrai_todos_os_arquivos()
    converte_todos_txt_csv()
    dados2017, dados2018, dados2019 = joga_todos_dados_pandas()
    dados_enade = concat_anos([dados2017,dados2018,dados2019])
    dados_enade = filtra_dados_irreais(dados_enade)
    dados_enade = remove_duplicatas_curso(dados_enade)
    dados_enade = filtra_categorias(dados_enade)
    # dados_enade = filtra_grupos(dados_enade)
    banco = cria_banco(NOME_BANCO)
    carrega_banco(banco, dados_enade)
    relacao_genero_nota(dados_enade)
    relacao_instituicao_nota(dados_enade)
    relacao_curso_nota(dados_enade)
    


    
   


        