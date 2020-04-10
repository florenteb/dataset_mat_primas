
import pandas as pd
from tools import *

from bs4 import BeautifulSoup
#from selenium.webdriver.support.ui import Select
#from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
#from selenium.common.exceptions import UnexpectedAlertPresentException as WDE
#from selenium.common.exceptions import TimeoutException as WDE_TimeOut

def Chrome_driver():
    # Chrome driver for development and text use
    from selenium import webdriver
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('--log-level=3') 
    browser = webdriver.Chrome(chrome_options=options)
    return browser

def Phantom_driver():
    from selenium import webdriver
    
    # User-agent change
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36' 
    cap = webdriver.DesiredCapabilities.PHANTOMJS
    cap["phantomjs.page.settings.userAgent"] = user_agent
    browser = webdriver.PhantomJS(desired_capabilities=cap)
    #browser = webdriver.PhantomJS()
    return browser

def Close_driver(browser):
    browser.close()
    print('Closing connection')

def Set_Mercado_Filter(browser, mercado_value):
    mercado = browser.find_elements_by_id('markets_filter')
    for option in mercado[0].find_elements_by_tag_name('option'):
        if option.text == mercado_value:
            option.click()
            break
    return str(option.text)

def Set_Start_Date(browser,fecha):
    fecha_inicio = browser.find_element_by_id('from_filter')
    fecha_inicio.send_keys(fecha)
    return fecha_inicio.get_attribute('value')

def Set_End_Date(browser, fecha):
    fecha_fin = browser.find_element_by_id('to_filter')
    fecha_fin.send_keys(fecha)
    return fecha_fin.get_attribute('value')

def Loading_dataset(browser, columns_name):
    ds = pd.DataFrame(columns=columns_name)
    
    return (ds)

def Scraping_MercaMardrid(br, mercado, fecha_inicio, fecha_fin):
    if br=='Phantom':
        browser = Phantom_driver()
    elif br=='Chrome':
        browser = Chrome_driver()
    else:
        browser = Phantom_driver()
        
    url ='https://www.mercamadrid.es/estadisticas/'
    browser.implicitly_wait(60)
    browser.get(url)
    #print('')
    #print('MercaMadrid Data Extractor')
    #print('--------------------------')
    #'MERCADO CENTRAL DE FRUTAS'
    print('Mercado: ' + Set_Mercado_Filter(browser, mercado),
        'Fecha inicio: ' + Set_Start_Date(browser, fecha_inicio),
        'Fecha fin: ' + Set_End_Date(browser, fecha_fin)
        )
    print('------------')
    print('Waiting for webpage')
    
    browser.find_element_by_id("btnBuscar").submit()
    condition= EC.visibility_of_element_located((By.CLASS_NAME,'estadisticas-zima-lista'))
    WebDriverWait(browser, 60).until(condition)
    columns_name=['Producto', 'kilos producto', 'Variedad', 'Kilos variedad', 'Precio max', 'Precio min', 'Precio frecuente']
    #ds=pd.DataFrame(Loading_dataset(browser,columns_name))

    page = BeautifulSoup(browser.page_source, "html.parser")
    lista = page.find_all('div', class_='estadisticas-zima-lista-fila')
    #assert lista.count()!=0
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
    
    df=pd.DataFrame(row_list, columns=columns_name) 
     # New column with Year
    Año = [Extract_Year_from_date(fecha_inicio)] * len(df)
    df['Año']=Año

    # New column with Month
    Mes = [Extract_Month_from_date(fecha_inicio)] * len(df)
    df['Mes']=Mes
    
    # New columns with Data Source
    origen = ['MecaMadrid'] * len(df)
    df['Origen'] = origen
    
    #if br!='Phantom' : input ('Press ENTER to close the browser')
    Close_driver(browser)
    return(df)

    
    

# Main program    
if '__main__' == __name__:
    #Options for browser:  Phantom or Chrome'
    browser = 'Chrome'
    silence = True
    fecha_inicio='2020-01-01'
    fecha_fin = str(last_day_Month(fecha_inicio))
    df= Scraping_MercaMardrid(browser,'MERCADO CENTRAL DE FRUTAS', fecha_inicio, fecha_fin)
    print(df.head())
    print(df.shape())
    

    