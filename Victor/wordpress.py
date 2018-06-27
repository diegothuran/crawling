#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import requests
import json
import base64
import datetime
from time import gmtime, strftime
import string 

USER = b'admpolitica'
PASSWORD = b'xarx@2018'

URL = 'https://politica.xarx.rocks/wp-json/wp/v2'
# url_media = 'https://politica.xarx.rocks/wp-json/wp/v2/media'
# url_pernambuco = 'https://politica.xarx.rocks/pe/wp-json/wp/v2'

token = base64.standard_b64encode(USER + b':' + PASSWORD)
headers = {'Authorization': b'Basic ' + token}

# headers = {'Authorization': 'Basic ' + token,
#            'rel' : "https://api.w.org/"}

# headers = {
#         'Accept': 'application/json',
#         'Content-Type': 'application/json',
#         'Authorization': 'Basic ' + token
#     }

# headers = {
#             'Access-Control-Allow-Headers' : 'Authorization, Content-Type',
#             'Access-Control-Expose-Headers' : 'X-WP-Total, X-WP-TotalPages',
#             'Allow' : 'GET, POST, PUT, PATCH, DELETE',
#             'Cache-Control' : 'no-store, no-cache, must-revalidate', 
#             'Connection' : 'Keep-Alive',
# #             Content-Length →1757
#             'Content-Type' : 'application/json; charset=UTF-8',
# #             Date →Wed, 30 May 2018 12:46:27 GMT
# #             Expires →Wed, 11 Jan 1984 05:00:00 GMT
#             'Keep-Alive' : 'timeout=5, max=100',
# #             Link →<https://politica.xarx.rocks/pe/testando-basico-pe-am/>; rel="alternate"; type=text/html
#             'Pragma' : 'no-cache',
# #             Server →Apache/2.4.18 (Ubuntu)
#             'X-Content-Type-Options' : 'nosniff',
#             'X-Robots-Tag' : 'noindex',
#            'Authorization': 'Basic ' + token
#            }

# categoria sem_categoria : 1
# categoria geral : 67
INDEX_CATEGORIES = {'avante' : 16,  
                    'dc' : 22,
                    'dem' : 6,
                    'mdb' : 2,
                    'novo' : 34,
                    'psl' : 25,
                    'patri' : 31,
                    'pcb' : 19,
                    'pcdob' : 7,
                    'pco' : 23,
                    'pdt' : 4,
                    'phs' : 21,
                    'pmb' : 36,
                    'pmn' : 12,
                    'pode' : 24,
                    'pp' : 17,
                    'ppl' : 30,
                    'pps' : 14,
                    'pr' : 28,
                    'prb' : 26,
                    'pros' : 32,
                    'prp' : 13,
                    'prtb' : 20,
                    'psb' : 8,
                    'psc' : 11,
                    'psd' : 29,
                    'psdb' : 9,
                    'psol' : 27,
                    'pstu' : 18,
                    'pt' : 5,
                    'ptb' : 3,
                    'ptc' : 10,
                    'pv' : 15,
                    'rede' : 35,
                    'sd' : 33
                    }


def remove_punctuation(input_text):
    """
    Removes the punctuation from the input_text string
    python 2 (string.maketrans) is different from python 3 (str.maketrans)
    
    Parameters
    ----------
    input_text: string in which the punctuation will be removed
    
    Return
    ------
        input_text without the puncutation
    """
    # Make translation table
    punct = string.punctuation
    # if python 2
    trantab = str.maketrans(punct, len(punct)*' ')  # Every punctuation symbol will be replaced by a space
#     # if python 3
#     trantab = str.maketrans(punct, len(punct)*' ')  # Every punctuation symbol will be replaced by a space
    return input_text.translate(trantab)

def get_categories_idx(df, idx_noticia):
    """
    Get the wordpress categories index for the 'noticia' at idx_noticia index 
    
    Parameters
    ----------
    df : dataframe containing all the data
    idx_noticia:  index of the 'noticia'
    
    Return:
    ------
        categories_idx: list of the wordpress categories index for the 'noticia' at idx_noticia index 
    """
    categories_noticias = df['categorias']
    list_categories = remove_punctuation(categories_noticias[idx_noticia]).split()
    categories_idx = []
    for category in list_categories:
        if category in INDEX_CATEGORIES.keys():
            categories_idx.append(INDEX_CATEGORIES[category])
    return categories_idx  

def get_stations_idx(df, idx_noticia):
    """
    Get the wordpress stations index for the 'noticia' at idx_noticia index 
    
    Parameters
    ----------
    df : dataframe containing all the data
    idx_noticia:  index of the 'noticia'
    
    Return:
    ------
        stations: list of the wordpress stations for the 'noticia' at idx_noticia index 
    """
    stations_noticias = df['estacoes']
    list_stations = remove_punctuation(stations_noticias[idx_noticia]).split()
    return list_stations  

def get_categories_all_noticias(df):
    """
    Get the list of categories (list of categories (str)) for all 'noticias' 
    
    Parameters
    ----------
    df : dataframe containing all the data
    
    Return:
    ------
        list_categorias: list of list of categories for all 'noticias'
    """
    categories_noticias = df['categorias']
    list_categories = []
    for categories_noticia in categories_noticias:
        list_categories.append(remove_punctuation(categories_noticia).split())
    return list_categories

def get_categorias_noticia(df, idx_noticia):
    """
    Get the categories (list of categories (str)) for 'noticia' at idx_noticia index 
    
    Parameters
    ----------
    df : dataframe containing all the data
    
    Return:
    ------
        list_categorias: lista de categorias para a noticia no indice idx_noticia
    """
    categories_noticias = df['categorias']
    list_categories = remove_punctuation(categories_noticias[idx_noticia]).split()
    return list_categories  

if __name__ == '__main__':            
    # columns = links, noticia, titulos, categorias, estacoes
    df = pd.read_csv('resultados-categorias-tag.csv')
    use_image = False
                      
#     for idx in range(len(df)):
    # idx for test = [14, 21, 22, 36]
    idx = 21
    # date now        
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # the wordpress categories index for the 'noticia' at idx_noticia index 
    categories = get_categories_idx(df, idx)
    # the wordpress stations for the 'noticia' at idx_noticia index
    stations = get_stations_idx(df, idx)
    print(stations)
    # the text of the 'noticia' and the link of the 'noticia'
    content = df['noticia'][idx] + '\n\nFonte: ' + '<a href=' + df['links'][idx] +'> ' + df['links'][idx] + '</a>' 
             
    # if the 'noticia' does not have category
    if(categories == []):
        categories.append(67) # category Geral
    print(categories)
      
# #     for station in stations:
#     # url for the choosen station
# #     url = 'https://politica.xarx.rocks/' + stations[0] + '/wp-json/wp/v2'
#     url = 'https://politica.xarx.rocks/pe/wp-json/wp/v2'
#     post_blogs = ['12', '13'] # estacao am
#     post = {'date': date,
#             'title': df['titulos'][idx],
#             'categories': categories,
#             'postBlogs': post_blogs,
#             'status': 'publish',
#             'content': content,
#             'author': '1',
#             'format': 'standard'
#             }
#                        
#     r = requests.post(url + '/posts', headers=headers, json=post)
#     print('POST = ' + str(r))
    
    # url for the choosen station
    url = 'https://politica.xarx.rocks/' + stations[0] + '/wp-json/wp/v2'
#             url_pernambuco = 'https://politica.xarx.rocks/pe/wp-json/wp/v2'
    post = {'date': date,
            'title': df['titulos'][idx],
            'categories': categories,
            'postBlogs': [7],
#             'slug': 'post-sao-paulo',
            'status': 'publish',
            'content': content,
            'author': '1',
            'format': 'standard'
            }
                     
    r = requests.post(url + '/posts', headers=headers, json=post)
    print('POST = ' + str(r))
           
    if(use_image): 
        media = {'file': open('recife.png','rb'), 'caption': 'picture'}
        image = requests.post(url + '/media', headers=headers, files=media)        
            
        img_id = requests.get(url + '/media').json()[0]['id']
        post_id = requests.get(url + '/posts').json()[0]['id']
                
        updated_post = {'featured_media' : img_id}
                 
        update = requests.post(url + '/posts/' + str(post_id), headers=headers, json=updated_post)     
        print('UPDATE_POST = ' + str(update))
            
#     # testing get request
#     url_get = 'https://politica.xarx.rocks/pr/wp-json/wp/v2'
#     r = requests.get(url_get + '/posts')
#     print(r.json()[0]['id'])
#     
#     update = requests.post(url_get + '/posts/' + str(41))
#     print('UPDATE_POST = ' + str(update))
