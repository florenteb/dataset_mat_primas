'''
    Scraping MercAlicante
'''

import time
from tqdm import tqdm

import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO

def Loading_dataset(columns_name):
        
    ds = pd.DataFrame(columns=columns_name)
    page = BeautifulSoup(browser.page_source, "html.parser")
    lista = page.find_all('div', class_='estadisticas-zima-lista-fila')
    
    row_list=[]
    
    for elemento in lista:
        my_dict={}
        my_dict.update({
            'Producto':elemento.find('div', class_='estadisticas-zima-lista-celda-1').text,
            'kilos producto':elemento.find('div', class_='estadisticas-zima-lista-celda-2').text,
            'Variedad':elemento.find('div', class_='estadisticas-zima-lista-celda-3').text,
            'Kilos variedad':elemento.find('div', class_='estadisticas-zima-lista-celda-4').text,
            'Precio max':elemento.find('div', class_='estadisticas-zima-lista-celda-5').text,
            'Precio min':elemento.find('div', class_='estadisticas-zima-lista-celda-6').text,
            'Precio frecuente':elemento.find('div', class_='estadisticas-zima-lista-celda-7').text
        })
        row_list.append(my_dict)
    
    ds=pd.DataFrame(row_list, columns=columns_name) 
    
    return (ds)

def url_compose(url, Producto, Familia, Categoria, Fecha_inicio, Fecha_fin):
    url = url + 'producto=' + Producto
    url = url + '&familia=' + Familia
    url = url + '&categoria=' + Categoria
    url = url + '&desde=' + Fecha_inicio
    url = url + '&hasta=' + Fecha_fin
    return url

producto='' #Void all products
familia='' # Void all families
categoria = '106' # Frutas
fecha_Inicio = '2020-03-01'
fecha_Fin = '2020-03-22'
url = 'https://www.mercalicante.com/ajax/ajax-obtener-precios.php?'

# Main program    
if '__main__' == __name__:

    print('')
    print('MercAlicante Data Extractor')
    print('--------------------------')
    print('Product: ' + producto ) 
    print('Family: ' + familia ) 
    print('Category: ' + categoria + ' - Frutas')
    print('Start Date: ' + fecha_Inicio ) 
    print('End Date: ' + fecha_Fin )
    print('------------')

    url= url_compose(url, producto, familia, categoria, fecha_Inicio, fecha_Fin)
    print('Waiting for webpage')
    resp = requests.get(url)
    resp.content

    columns_name =['Producto','Variedad','Maximo','Minimo','Frecuente']
    
    list = pd.read_html(url) # Returns list of all tables on page
    #ds.columns= columns_name
    table = pd.concat(list)
    table.columns= columns_name
    print(table)
    



#
#    ds=pd.DataFrame(Loading_dataset(columns_name))

#    print('------------')
#    print(ds)

