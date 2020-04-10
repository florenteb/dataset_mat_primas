'''
    Scraping MercAlicante
    =====================
    Extract vegetable price by month of Central Market Merca Alicante
    web site: https:\\www.mercalicante.com
    Creation Date: 2020/04/10
    
'''

import requests
import pandas as pd
from tools import *

def url_compose(url, Producto, Familia, Categoria, Fecha_inicio, Fecha_fin):
    url = url + 'producto=' + Producto
    url = url + '&familia=' + Familia
    url = url + '&categoria=' + Categoria
    url = url + '&desde=' + Fecha_inicio
    url = url + '&hasta=' + Fecha_fin
    return url

def Scraping_MercAlicante(producto, familia, categoria, fecha_Inicio, fecha_Fin):
    url = 'https://www.mercalicante.com/ajax/ajax-obtener-precios.php?'
    print('')
    #print('MercAlicante Data Extractor')
    #print('--------------------------')
    
    print('Product: ' + 'None' if producto == ''else producto,
        'Family: ' + 'None' if familia == '' else familia,
        'Category: ' + categoria, 
        'Start Date: ' + fecha_Inicio, 'End Date: ' + fecha_Fin  ) 
    print('------------')
    # Call to Url compose function
    url= url_compose(url, producto, familia, categoria, fecha_Inicio, fecha_Fin)
    print('Waiting for webpage')

    resp = requests.get(url)
    if (resp.status_code != 200):
        print("Error al obtener datos: ", resp)

    columns_name =['Producto','Variedad','Maximo','Minimo','Frecuente']
    
    list = pd.read_html(url) # Returns list of all tables on page
    table = pd.concat(list)
    table.columns= columns_name

    # New column with Year
    Año = [Extract_Year_from_date(fecha_Inicio)] * len(table)
    table['Año']=Año

    # New column with Month
    Mes = [Extract_Month_from_date(fecha_Inicio)] * len(table)
    table['Mes']=Mes

    # New columns with Data Source
    origen = ['MecAlicante'] * len(table)
    table['Origen'] = origen
    
    return (table)

# Main program    
if '__main__' == __name__:
    producto='' #Void all products
    familia='' # Void all families
    categoria = '106' # Frutas
    fecha_Inicio = '2020-03-01'
    # last day of the month or current day
    fecha_Fin = str(last_day_Month(fecha_Inicio))
    df_Mercalicante = Scraping_MercAlicante(producto, familia, 
        categoria, fecha_Inicio, fecha_Fin)
    
    print(df_Mercalicante)




    

