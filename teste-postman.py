import pandas as pd
import requests
import json
import base64
import datetime
from time import gmtime, strftime
import string
import numpy as np

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

# faltando 'ce'
INDEX_STATIONS = {'ac' : 2,
                  'al' : 3,
                  'ap' : 4,
                  'ba' : 6,
                  'am' : 7,
                  'df' : 8,
                  'es' : 9,
                  'go' : 10,
                  'ma' : 11,
                  'mt' : 12,
                  'ms' : 13,
                  'mg' : 14,
                  'pa' : 15,
                  'pb' : 16,
                  'pr' : 17,
                  'pe' : 18,
                  'pi' : 19,
                  'rj' : 20,
                  'rn' : 21,
                  'rs' : 22,
                  'ro' : 23,
                  'rr' : 24,
                  'sc' : 25,
                  'sp' : 26,
                  'se' : 27,
                  'to' : 28
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
    trantab = str.maketrans(punct, len(punct) * ' ')  # Every punctuation symbol will be replaced by a space
    #     # if python 3
    #     trantab = str.maketrans(punct, len(punct)*' ')  # Every punctuation symbol will be replaced by a space
    return input_text.translate(trantab)


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

def join_strings(list_of_strings):
    """
        Método para transformar tokens em uma única sentença
    :param list_of_strings: Lista com os tokens
    :return: sentença formada pela união dos tokens
    """
    return ", ".join(list_of_strings)


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
    stations_idx = [INDEX_STATIONS[station] for station in list_stations]
    return list_stations, stations_idx


df = pd.read_csv('/home/diego/Dropbox/Python/crawling/Politica/src/Data/news/resultados-categorias-tag.csv')
use_image = True

#     for idx in range(len(df)):
idx = 6
if (df['estacoes'][idx] != '{}'):
    # date now
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # the wordpress categories index for the 'noticia' at idx_noticia index
    categories = get_categories_idx(df, idx)
    # the wordpress stations for the 'noticia' at idx_noticia index
    stations, stations_idx = get_stations_idx(df, idx)
    # stations to replicate
    post_blogs = stations_idx[1:]
    # the text of the 'noticia' and the link of the 'noticia'
    content = df['noticia'][idx] + '\n\nFonte: ' + '<a href=' + df['links'][idx] + '> ' + df['links'][idx] + '</a>'

    # if the 'noticia' does not have category
    if (categories == []):
        categories.append(67)  # category Geral

    # url for the choosen station
    url = 'https://politica.xarx.rocks/' + stations[0] + '/wp-json/wp/v2'
    #         url_pernambuco = 'https://politica.xarx.rocks/pe/wp-json/wp/v2'
    payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; \
    name=\"title\"\r\n\r\n{0}\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: \
    form-data; name=\"categories\"\r\n\r\n{1}\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: \
    form-data; name=\"content\"\r\n\r\n{2}\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: \
    form-data; name=\"status\"\r\n\r\npublish\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: \
    form-data; name=\"postBlogs\"\r\n\r\n{3}\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--".format(df['titulos'][0],
                                                                                                  join_strings(np.array(
                                                                                                      categories[
                                                                                                          0]).astype(
                                                                                                      str).tolist()),
                                                                                                  content,
                                                                                                  stations).encode(
        "utf-8")

    headers = {
        'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
        'authorization': "Basic YWRtcG9saXRpY2E6eGFyeEAyMDE4",
        'cache-control': "no-cache",
        'postman-token': "660515d7-2398-f142-2660-69ff2d5ef344"
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)

    if (use_image):
        image_path = 'images/' + df['image'][idx]
        media = {'file': open(image_path, 'rb'), 'caption': 'picture'}
        image = requests.post(url + '/media', headers=headers, files=media)

        img_id = requests.get(url + '/media').json()[0]['id']
        post_id = requests.get(url + '/posts').json()[0]['id']

        updated_post = {'featured_media': img_id}

        update = requests.post(url + '/posts/' + str(post_id), headers=headers, json=updated_post)
        print('UPDATE_POST = ' + str(update))
