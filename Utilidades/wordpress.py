#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import requests
import json
import base64
import datetime
from time import gmtime, strftime
import string 

USER = 'admpolitica'
PASSWORD = 'xarx@2018'
url = 'https://politica.xarx.rocks/wp-json/wp/v2'
url_media = 'https://politica.xarx.rocks/wp-json/wp/v2/media'

token = base64.standard_b64encode(USER + ':' + PASSWORD)
headers = {'Authorization': 'Basic ' + token}

#categoria sem_categoria : 1
#categoria geral : 97
INDEX_CATEGORIES = {#ESTADOS
                    'ac' : 70,
                    'al' : 71,
                    'ap' : 72,
                    'am' : 73,
                    'ba' : 74,
                    'ce' : 75,
                    'df' : 76,
                    'es' : 77,
                    'go' : 78,
                    'ma' : 79,
                    'mt' : 80,
                    'ms' : 81,
                    'mg' : 82,
                    'pa' : 83,
                    'pb' : 84,
                    'pr' : 85,
                    'pe' : 86,
                    'pi' : 87,
                    'rj' : 88,
                    'rn' : 89,
                    'rs' : 90,
                    'ro' : 91,
                    'rr' : 92,
                    'sc' : 93,
                    'sp' : 94,
                    'se' : 95,
                    'to' : 96,
                    #PARTIDOS
                    'pdt' : 105,
                    'pcdob' : 106,
                    'dem' : 108,
                    'pmdb' : 109,
                    'pps' : 110,
                    'pp' : 111,
                    'psdb' : 44,
                    'psb' : 45,
                    'pt' : 46,
                    'pstu' : 47,
                    'pv' : 48,
                    'ptb' : 49,
                    'pcb' : 112,
                    'psol' : 51,
                    'prtb' : 52,
                    'psd' : 53,
                    'ptdob' : 54,
                    'ptc' : 55,
                    'psl' : 56,
                    'psc' : 57,
                    'psdc' : 58,
                    'pmn' : 113,
                    'pco' : 114,
                    'prp' : 115,
                    'phs' : 116,
                    'prb' : 117,
                    'ppl' : 118,
                    'pros' : 119,
                    'pen' : 120,
                    'rede' : 67,
                    'pmb' : 121
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
    # columns = links, noticia, titulos, categorias
    df = pd.read_csv('../Data/resultados-categorias.csv')
    use_image = False
             
    for idx in range(len(df)):
#     for idx in range(30):
        # date now        
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # the wordpress categories index for the 'noticia' at idx_noticia index 
        categories = get_categories_idx(df, idx)
        # the text of the 'noticia' and the link of the 'noticia'
        content = df['noticia'][idx] + '\n\nFonte: ' + df['links'][idx]
            
        # if the 'noticia' does not have category
        if(categories == []):
            #categoria geral : 97
            categories.append(97)        
        print(categories)
            
        post = {'date': date,
                'title': df['titulos'][idx],
                'categories': categories,
#                 'slug': 'post-sao-paulo',
                'status': 'publish',
                'content': content,
                'author': '1',
                'format': 'standard'
                }
                     
        r = requests.post(url + '/posts', headers=headers, json=post)
        print('POST = ' + str(r))
         
        if(use_image): 
            # ver como é que vai vir a imagem para ajeitar no open
            media = {'file': open('pernambuco.png','rb'), 'caption': 'picture'}
            image = requests.post(url + '/media', headers=headers, files=media)        
             
            img_src = requests.get(url + '/media').json()[0]['source_url']
            post_id = requests.get(url + '/posts').json()[0]['id']
            content = requests.get(url + '/posts').json()[0]['content']['rendered']
            updated_content = '<img src=' + img_src + '>' + content
            updated_post = {'content': updated_content}
               
            update = requests.post(url + '/posts/' + str(post_id), headers=headers, json=updated_post)     
            print('UPDATE_POST = ' + str(update))
         
#     # testing get request
#     r = requests.get(url + '/posts')
#     print(r.json()[0])
