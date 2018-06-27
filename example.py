import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import os
from Util import check_news, download_image
import urllib3

def join_strings(list_of_strings):
    """
        Método para transformar tokens em uma única sentença
    :param list_of_strings: Lista com os tokens
    :return: sentença formada pela união dos tokens
    """
    return "<p>".join(list_of_strings)


#Função para o Web crawler
def web_crawler(url_partida, limite_links):
    if os.path.exists('resultados-uol2.csv'):
        resultados = pd.read_csv('resultados-uol2.csv')
    else:
        resultados = pd.DataFrame({'titulos': [], 'links': [], 'noticia': [], 'image': []})
        
        
    for j in range(1, int(limite_links/10)+1):
        lista_links.append(url_partida + "#?next=0001H1294U" + str(30 * j) + "N")


    #Recupera o código fonte da URL
    fonte = requests.get(url_partida)
    fonte_bs = BeautifulSoup(fonte.text)
    #Para o componente com a classe widget-news-list recupere todas as tags 'a' cujo conteúdo 'href' seja um endereço http válido
    links_coletados = fonte_bs.find('div', class_='itens-indice').find_all('span', class_='titulo', limit=None)
    links_links = fonte_bs.find('div', class_='itens-indice').find_all('a')

    #Para cada link recuperado
    for titulo, link in zip(links_coletados, links_links):
        row = {'titulos': [], 'links': [], 'noticia': [], 'image': []}
        row['titulos'].append(titulo.contents[0])
        row['links'].append(link.get('href'))

        print(str(titulo.contents[0]))

        if not check_news(resultados, str(titulo.contents[0])):
            link_ = link.get('href')
            req = requests.get(link_)

            try:
                bs = BeautifulSoup(req.text).find('div', id= 'texto').find_all('p')
                images = BeautifulSoup(req.text).find('div', id= 'texto').find_all('img')
                src = images[0].get('src')
                path_image = os.path.split(src)[-1]
                noticia = []
                row['image'].append(path_image)
                download_image(src, os.path.join('images', path_image))
                for p in bs:
                    text = p.contents[0]
                    if isinstance(text, str):
                        noticia.append(p.contents[0])
                row['noticia'].append(join_strings(noticia))
            except:
                try:
                    bs = BeautifulSoup(req.text).find('div', class_='desc').find_all('p', class_='text-description')
                    noticia = []
                    for p in bs:
                        text = p.contents[0]
                        if isinstance(text, str):
                            noticia.append(p.contents[0])
                    row['noticia'].append(join_strings(noticia))
                    row['image'].append(0)
                except:
                    try:
                        bs = BeautifulSoup(req.text).find('article', class_='l-content-text__container').find_all('p')
                        #
                        images = BeautifulSoup(req.text).find('div', id='l-content-text__head--medial-content-text__head--media').find_all('img')
                        src = images[0].get('src')
                        path_image = os.path.split(src)[-1]
                        noticia = []
                        row['image'].append(path_image)
                        download_image(src, os.path.join('images', path_image))
                        for l in range(len(bs)-1):
                            text = bs[l].contents[0]
                            if isinstance(text, str):
                                noticia.append(p.contents[0])
                        row['noticia'].append(join_strings(noticia))
                        row['image'].append(0)
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
                            row['noticia'].append(join_strings(noticia))
                            row['image'].append(0)
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
                                row['noticia'].append(join_strings(noticia))
                                row['image'].append(0)
                            except:
                                row['noticia'].append(0)
                                row['image'].append(0)
            try:
                row = pd.DataFrame(row)
                resultados = resultados.append(row)
            except:
                pass



    for url in lista_links:
        row = {'titulos': [], 'links': [], 'noticia': []}
        try:
            wd = webdriver.Chrome('Utilidades/chromedriver')
            wd.get(url)
            fonte_pagina = wd.page_source
            print("aqui")
            wd.quit()
            soup = BeautifulSoup(fonte_pagina)
            links_coletados = soup.find('div', class_='itens-indice').find_all('span', limit=None)
            links_links = soup.find('div', class_='itens-indice').find_all('a')
            for titulo, link in zip(links_coletados, links_links):
                row = {'titulos': [], 'links': [], 'noticia': [], 'image': []}
                row['titulos'].append(titulo.contents[0])
                row['links'].append(link.get('href'))

                print(str(titulo.contents[0]))

                if not check_news(resultados, str(titulo.contents[0])):
                    link_ = link.get('href')
                    req = requests.get(link_)

                    try:
                        bs = BeautifulSoup(req.text).find('div', id='texto').find_all('p')
                        images = BeautifulSoup(req.text).find('div', id='texto').find_all('img')
                        src = images[0].get('src')
                        path_image = os.path.split(src)[-1]
                        noticia = []
                        row['image'].append(path_image)
                        download_image(src, os.path.join('images', path_image))
                        for p in bs:
                            text = p.contents[0]
                            if isinstance(text, str):
                                noticia.append(p.contents[0])
                        row['noticia'].append(join_strings(noticia))
                    except:
                        try:
                            bs = BeautifulSoup(req.text).find('div', class_='desc').find_all('p',
                                                                                             class_='text-description')
                            noticia = []
                            for p in bs:
                                text = p.contents[0]
                                if isinstance(text, str):
                                    noticia.append(p.contents[0])
                            row['noticia'].append(join_strings(noticia))
                            row['image'].append(0)
                        except:
                            try:
                                bs = BeautifulSoup(req.text).find('article',
                                                                  class_='l-content-text__container').find_all('p')
                                #
                                images = BeautifulSoup(req.text).find('div',
                                                                      id='l-content-text__head--medial-content-text__head--media').find_all(
                                    'img')
                                src = images[0].get('src')
                                path_image = os.path.split(src)[-1]
                                noticia = []
                                row['image'].append(path_image)
                                download_image(src, os.path.join('images', path_image))
                                for l in range(len(bs) - 1):
                                    text = bs[l].contents[0]
                                    if isinstance(text, str):
                                        noticia.append(p.contents[0])
                                row['noticia'].append(join_strings(noticia))
                                row['image'].append(0)
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
                                    row['noticia'].append(join_strings(noticia))
                                    row['image'].append(0)
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
                                        row['noticia'].append(join_strings(noticia))
                                        row['image'].append(0)
                                    except:
                                        row['noticia'].append(0)
                                        row['image'].append(0)
                    try:
                        row = pd.DataFrame(row)
                        resultados = resultados.append(row)
                    except:
                        pass
        except:
            pass

    return resultados

#Função para o Web scraper
def web_scraper(link, output_path):
    #Para cada link armazenado na lista de links
    for link in lista_links:
        #Recupera o código fonte
        fonte = requests.get(link)
        fonte_bs = BeautifulSoup(fonte.text, 'lxml')
        #Faz a raspagem das imagens
        imagens = fonte_bs.find_all('img')

        #Para cada imagem coletada do link
        for imagem in imagens:
            #Apresenta o código da imagem raspado
            print(imagem)
            print("\n")
        print("\n")


#Inicia a lista_links
lista_links = []
#Define que o limite será de 10 links coletados
limite_links = 20
#Define a URL de partida
url_partida = 'https://noticias.uol.com.br/politica/eleicoes/ultimas/'

#Chamada para a função do Web crawler
titulos = web_crawler(url_partida, limite_links)
df = pd.DataFrame(titulos)
df.to_csv('resultados-uol2.csv')
