#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import string 


ESTADOS = ['acre', 'alagoas', 'amapá', 'amazonas', 'bahia', 'ceará', 'distrito federal',  'espírito santo',  'goiás',  
           'maranhão', 'mato grosso',  'mato grosso do sul',  'minas gerais',  'pará',  'paraíba',  'paraná',  'pernambuco',  
           'piauí',  'rio de janeiro', 'rio grande do norte', 'rio grande do sul', 'rondônia', 'roraima', 'santa catarina', 
           'são paulo', 'sergipe', 'tocantins']

CAPITAIS = ['rio branco', 'maceió', 'macapá', 'manaus', 'salvador', 'fortaleza', 'brasília', 'vitória', 'goiânia', 'são luís',
            'cuiabá', 'campo grande', 'belo horizonte', 'belém', 'joão pessoa', 'curitiba', 'recife', 'teresina', 'rio de janeiro',
            'natal', 'porto alegre', 'porto velho', 'boa vista', 'florianópolis', 'são paulo', 'aracaju', 'palmas']

SIGLAS_ESTADOS = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA','PB', 'PR', 
                  'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE','TO'] 

# https://www.suapesquisa.com/partidos/
PARTIDOS = ['partido democrático trabalhista', 'partido comunista do brasil', 'democratas', 
            'movimento democrático brasileiro', 'partido popular socialista', 'partido progressista', 
            'partido da social democracia brasileira', 'partido socialista brasileiro', 'partido dos trabalhadores', 
            'partido socialista dos trabalhadores unificado', 'partido verde', 'partido trabalhista brasileiro', 
            'partido comunista brasileiro', 'partido socialismo e liberdade', 'partido renovador trabalhista brasileiro', 
            'partido social democrático', 'partido trabalhista do brasil', 'partido trabalhista cristão', 'partido social liberal', 
            'partido social cristão', 'partido social democrata cristão', 'partido da mobilização nacional', 'partido da causa operária', 
            'partido republicano progressista', 'partido humanista da solidariedade', 'partido republicano brasileiro', 
            'partido pátria livre', 'partido republicano da ordem social', 'partido ecológico nacional', 'rede sustentabilidade', 
            'partido da mulher brasileira', 'pc do b', 'pt do b', 'partido do movimento democrático brasileiro' ]

# partido do movimento democrático brasileiro (pmdb) = Movimento Democrático Brasileiro (MDB)
# 'pcdob' and 'ptdob': just in SIGLAS_PARTIDOS, so len(SIGLAS_PARTIDOS) > len(PARTIDOS)
SIGLAS_PARTIDOS = ['pdt', 'pcdob', 'dem', 'mdb', 'pps', 'pp', 'psdb', 'psb', 'pt', 'pstu', 'pv', 'ptb', 'pcb', 
                   'psol', 'prtb', 'psd', 'ptdob', 'ptc', 'psl', 'psc', 'psdc', 'pmn', 'pco', 'prp', 'phs', 'prb', 'ppl', 
                   'pros', 'pen', 'rede', 'pmb', 'pcdob', 'ptdob', 'pmdb']

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


def set_categories(df):
    """
    Set the categories for the noticias.
    Adds the 'categorias' column to the dataframe
    
    Parameters
    ----------
    df : dataframe containing all the data
    
    Return
    ------
        Dataframe with the new 'categorias' column added
        set_cats: list of set of categories
    """
    noticias = df['noticia']
    cats = []
    for idx_noticia in range(len(noticias)):
        cats_by_text = []

        # Removing punctuation 
        text = remove_punctuation(noticias[idx_noticia])
        # Primeiro ver as Siglas dos Estados para depois colocar para minusculo  
        words = text.split()
        for word in words:
            if word in SIGLAS_ESTADOS:   
                cats_by_text.append(word.lower())
                
        # text to lower case
        text = text.lower()   
        
        # seek for ESTADOS name
        for idx_estado in range(len(ESTADOS)):    
            if ESTADOS[idx_estado] in text: 
                cats_by_text.append(SIGLAS_ESTADOS[idx_estado].lower())
                
        # seek for CAPITAIS name
        for idx_capitais in range(len(CAPITAIS)):    
            if CAPITAIS[idx_capitais] in text: 
                cats_by_text.append(SIGLAS_ESTADOS[idx_capitais].lower())
                
        # Seek for PARTIDOS name
        for idx_partidos in range(len(PARTIDOS)):     
            if PARTIDOS[idx_partidos] in text:
                cats_by_text.append(SIGLAS_PARTIDOS[idx_partidos])
        
        # Seek for PARTIDOS sigla
        words = text.split()
        for word in words:
            if word in SIGLAS_PARTIDOS:  
                cats_by_text.append(word) 
        
        # Standardizing PMDB and MDB for the acronym PMDB
        cats_by_text = ['pmdb' if x=='mdb' else x for x in cats_by_text]
#         print(cats_by_text)
        cats.append(cats_by_text)
    # Removing replicated items
    set_cats = [set(cat) for cat in cats]
    df = df.assign(categorias = set_cats)
    return df, set_cats

if __name__ == '__main__':
    # columns = links, noticia, titulos, categorias   
    df = pd.read_csv('../resultados-uol2.csv', index_col=0)
#     noticias = df['noticia']
#     print(noticias[29])
    df, set_cats = set_categories(df)
    df.to_csv('../resultados-categorias.csv', encoding='utf-8')
               
    name_file = 'categorias.txt' 
    print('Writing table file')
    f = open(name_file, 'w')
    for idx_cats in range(len(set_cats)):
        f.write('\n' + str(idx_cats) + ' - categorias: ' + str(set_cats[idx_cats]))
    f.close() 
    print('End file')   
    
#     df = pd.read_csv('../Data/resultados-categorias.csv', index_col=0)
#     noticias = df['noticia']
#     print(noticias[29])
