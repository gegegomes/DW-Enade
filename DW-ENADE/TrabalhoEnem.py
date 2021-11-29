import requests
import os.path

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

if __name__ == "__main__":
    baixar_arquivo(URL_ENADE_2019 , NOME_ARQUIVO_ENADE_2019)
    baixar_arquivo(URL_ENADE_2018 , NOME_ARQUIVO_ENADE_2018)
    baixar_arquivo(URL_ENADE_2017 , NOME_ARQUIVO_ENADE_2017)