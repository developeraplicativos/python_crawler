import re
import threading

import requests
from bs4 import BeautifulSoup

DOMINIO = 'https://django-anuncios.solyd.com.br'
URL_AUTO = 'https://django-anuncios.solyd.com.br/automoveis/'
URL_CEL = 'https://django-anuncios.solyd.com.br/celulares/'
URL_ELET = 'https://django-anuncios.solyd.com.br/eletronicos/'
URL_IMOVEIS = 'https://django-anuncios.solyd.com.br/imoveis/'

LINKS = []
TELEFONES = []

def requisicao(url):
    try:
        resposta = requests.get(url)
        if( resposta.status_code == 200 ):
            return resposta.text
        else:
            raise Exception('Não conseguiu estabelecer conexão')
    except Exception as error:
        print('Error')
        print(error)

def parser(resposta):
    try:
        return BeautifulSoup(resposta, 'html.parser')
    except Exception as error:
        print('Error ao codding html')
        print(error)

def encontrar_link(soup):

    try:
        cards = soup.find("div", class_="ui three doubling link cards")
        links = cards.find_all('a')

        list_links = []
        for link in links:
            list_links.append(link['href'])

        return list_links

    except Exception as error:
        print(error)






def encontrar_telfone(soup):
    try:
        desc = soup.find_all("div", class_="sixteen wide column")[2].p.get_text().strip()
        result_rege = re.findall(r"\(?0?([1-9]{2})[ \-\.\)]{0,2}(9[ \-\.]?\d{4})[ \-\.]?(\d{4})",desc)
        if result_rege:
            return result_rege

    except Exception as error:
        print(error)
        return None

def descobrir_telefones():
    while True:
        try:
            link = LINKS.pop(0)
        except Exception:
            return None
        resposta_anuncio = requisicao(DOMINIO + link)
        if resposta_anuncio:
            soup_anuncio = parser(resposta_anuncio)
            if soup_anuncio:
                telefones = encontrar_telfone(soup_anuncio)
                if telefones:
                    for telefone in telefones:
                        print('telefone encontrado: {}'.format(telefone))
                        TELEFONES.append(telefone)
                        salvar_resultados(telefone)

def salvar_resultados(telefone):
    string_telefone = "{}{}{}\n".format(telefone[0], telefone[1], telefone[2])
    try:
        with open('telefones.txt','a') as arquivo:
            arquivo.write(str(string_telefone))
    except:
        print('erro ao salvar telefone')

if __name__ == "__main__":
    resposta_busca = requisicao(URL_AUTO)
    if resposta_busca:
        soup_busca = parser(resposta_busca)
        if soup_busca:
            LINKS = encontrar_link(soup_busca)

            THREADS = []
            for i in range(3):
                t = threading.Thread(target=descobrir_telefones)
                THREADS.append(t)

            for t in THREADS:
                t.start()

            for t in THREADS:
                t.join()