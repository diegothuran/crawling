#Conjunto de importações
#Classe para definir condição de espera para o WebDriver.
from selenium.webdriver.support.ui import WebDriverWait

#Conjunto de funções que determinam condições para a manipulação de elementos
from selenium.webdriver.support import expected_conditions as EC

#Classe utilizada para definir a localização do elemento a ser raspado
from selenium.webdriver.common.by import By

from selenium import webdriver
from bs4 import BeautifulSoup

#Definição da url        
url = 'https://noticias.uol.com.br/politica/eleicoes/ultimas/#?next=0001H1294U30N'


#Classes para os WebDrivers disponíveis.
#Descomente a linha referente ao seu navegador.
#wd = webdriver.Firefox()
wd = webdriver.Chrome('Utilidades/chromedriver')
#wd = webdriver.Safari()
#wd = webdriver.Edge()

#Carrega a página definida no url
wd.get(url)

#Durante 10s o WebDriver irá aguardar que a div 'glbComentarios-conteudo-interno' esteja clicável.
#WebDriverWait(wd, 10).until(
#    EC.element_to_be_clickable((By.XPATH, '//div[@class="filtro-paginacao"]')))
#Recupera o código-fonte da página
fonte_pagina = wd.page_source

#Encerra a instância aberta do navegador
wd.quit()

#Realiza a raspagem dos dados
soup = BeautifulSoup(fonte_pagina)
links_coletados = soup.find('div', class_='itens-indice').find_all('span', limit=None)
comentarios = soup.findAll('a', class_='nav pages next')
