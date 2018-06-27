import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import urllib3


def join_strings(list_of_strings):
    """
        Método para transformar tokens em uma única sentença
    :param list_of_strings: Lista com os tokens
    :return: sentença formada pela união dos tokens
    """
    return " ".join(list_of_strings)



def extract_news(titulo, link):
    resultado = {'titulo': [], 'link': []}
    resultado['titulo'].append(titulo.contents[0])
    resultado['links'].append(link.get('href'))
    link_ = link.get('href')
    print(link_)
    req = requests.get(link_)

    try:
        bs = BeautifulSoup(req.text).find('div', id='texto').find_all('p')
        noticia = []
        for p in bs:
            text = p.contents[0]
            if isinstance(text, str):
                noticia.append(p.contents[0])
        resultado['noticia'].append(join_strings(noticia))
    except:
        try:
            bs = BeautifulSoup(req.text).find('div', class_='desc').find_all('p', class_='text-description')
            noticia = []
            for p in bs:
                text = p.contents[0]
                if isinstance(text, str):
                    noticia.append(p.contents[0])
            resultado['noticia'].append(join_strings(noticia))
        except:
            try:
                bs = BeautifulSoup(req.text).find('article', class_='l-content-text__container').find_all('p')
                noticia = []
                for l in range(len(bs) - 1):
                    text = bs[l].contents[0]
                    if isinstance(text, str):
                        noticia.append(p.contents[0])
                resultado['noticia'].append(join_strings(noticia))
            except:
                try:
                    bs = BeautifulSoup(req.text).find('div',
                                                      class_='text').find_all(
                        'p')
                    noticia = []
                    for p in bs:
                        text = p.contents[0]
                        if isinstance(text, str):
                            noticia.append(p.contents[0])
                    resultado['noticia'].append(join_strings(noticia))
                except:
                    try:
                        bs = BeautifulSoup(req.text).find('div',
                                                          class_='c-news__body').find_all(
                            'p')
                        noticia = []
                        for p in bs:
                            text = p.contents[0]
                            if isinstance(text, str):
                                noticia.append(p.contents[0])
                        resultado['noticia'].append(join_strings(noticia))
                    except:
                        resultado['noticia'].append(0)

    return resultado


def check_news(data_frame=pd.DataFrame, string_busca=str):
    resp = False
    for index, row in data_frame.iterrows():
        if row['titulos'] == string_busca:
            resp = True
            break
        else:
            return False

    return resp

def download_image(url, path_to_save_image):
    http = urllib3.PoolManager()
    r = http.request('GET', url, preload_content=False)

    with open(path_to_save_image, 'wb') as out:
        while True:
            data = r.read(15)
            if not data:
                break
            out.write(data)

    r.release_conn()


