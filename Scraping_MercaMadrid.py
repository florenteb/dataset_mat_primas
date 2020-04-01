
import time
from tqdm import tqdm
import pandas as pd

from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException as WDE
from selenium.common.exceptions import TimeoutException as WDE_TimeOut

url ='https://www.mercamadrid.es/estadisticas/'
browser_visible=False

def Chrome_driver():
    # Chrome driver for development and text use
    from selenium import webdriver
    browser = webdriver.Chrome()
    browser_visible=True
    return browser

def Phantom_driver():
    from selenium import webdriver
    browser = webdriver.PhantomJS()
    browser_visible=False
    return browser

def Close_driver():
    browser.close()
    print('Closing connection')

def Set_Mercado_Filter(mercado_value):
    mercado = browser.find_elements_by_id('markets_filter')
    for option in mercado[0].find_elements_by_tag_name('option'):
        if option.text == mercado_value:
            option.click()
            break
    return str(option.text)

def Set_Start_Date(fecha):
    fecha_inicio = browser.find_element_by_id('from_filter')
    fecha_inicio.send_keys(fecha)
    return fecha_inicio.get_attribute('value')

def Set_End_Date(fecha):
    fecha_fin = browser.find_element_by_id('to_filter')
    fecha_fin.send_keys(fecha)
    return fecha_fin.get_attribute('value')

def Loading_dataset(columns_name):
        
    '''
    
    ''' 
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

# Main program    
if '__main__' == __name__:
    browser = Phantom_driver()
    #browser = Chrome_driver()
    browser.implicitly_wait(10)
    browser.get(url)

    print('')
    print('MercaMadrid Data Extractor')
    print('--------------------------')
    print('Filter 1: ' + Set_Mercado_Filter('MERCADO CENTRAL DE FRUTAS'))
    print('Filter 2: ' + Set_Start_Date('01/03/2020') ) 
    print('Filter 3: ' + Set_End_Date('25/03/2020'))
    print('------------')
    print('Waiting for webpage')

    browser.find_element_by_id("btnBuscar").submit()
    columns_name=['Producto', 'kilos producto', 'Variedad', 'Kilos variedad', 'Precio max', 'Precio min', 'Precio frecuente']
    ds=pd.DataFrame(Loading_dataset(columns_name))

    print('------------')
    print(ds)

    if browser_visible==True : print ('Press ENTER to close the browser')
    Close_driver()