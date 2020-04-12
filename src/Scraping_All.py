from tools import *
from Scraping_MercaAlicante import *
from Scraping_MercaMadrid import *
import datetime as dt
from time import time

def date_vector(año_inicio, año_fin, mes_inicio, mes_final, dia):
    # It generates a date vector with dates.
    # Output: a vector of strings 
    fecha=[]
    if año_inicio<= año_fin:
        if mes_inicio <= mes_final:
            for año in range(año_inicio, año_fin +1):
                for mes in range(mes_inicio,mes_final +1):
                    fecha.append(str(dt.date(año, mes, dia)))
    return(fecha)

def MercAlicante_scraper(producto, familia, categoria, fecha_inicio):
    print('MercAlicante Data Extractor')
    print('--------------------------')
    pos=1
    # Call to website by month
    try:
        for fecha in fecha_inicio:
            # Calculate the last day of the month or current day
            fecha_Fin = str(last_day_Month(fecha))
            df = Scraping_MercAlicante(producto, familia, 
                categoria, fecha, fecha_Fin)
            df_Mercalicante=df if pos==1 else pd.concat([df_Mercalicante, df])
            pos +=1
            
        #file_name= Save_df_to_csv(df_Mercalicante,'MercAlicante',fecha_inicio[0], str(last_day_Month(fecha_inicio[-1])))
        #return(file_name)
        return(df_Mercalicante)
    except:
        print('An error existing during MercAlicante extraction.')
        return(None)

def MercaMadrid_scraper(browser, mercado, fecha_inicio):
    # Date Extraction from MercaMadrid
    print('')
    print('MercaMadrid Data Extractor')
    print('--------------------------')
    pos=1
    try:
        # Call to website by month
        for fecha in fecha_inicio:
            fecha_fin = str(last_day_Month(fecha))
            df= Scraping_MercaMardrid(browser, mercado, fecha, fecha_fin)
            df_MercaMadrid = df if pos==1 else pd.concat([df_MercaMadrid, df])
            pos +=1
        #file_name=Save_df_to_csv(df_MercaMadrid,'MercaMadrid',fecha_inicio[0], str(last_day_Month(fecha_inicio[-1])))
        #return(file_name)
        return(df_MercaMadrid)
    except:

        return(None)

# Main program    
if '__main__' == __name__:
    # Generation of date vector
    # date_vector(fecha inicio, fecha fin, mes inicio, mes fin, dia)
    # Ex: ['2017-01-01', '2017-02-01', '2017-03-01'.... '2019-11-01', '2019-12-01']
    start_time = time()
    fecha_inicio = date_vector(2017, 2019, 1, 12, 1)
    #file_name_vector=[]
    columns = ['Producto','Precio','Año','Mes','Origen']
    df = pd.DataFrame(columns=columns)    
    if 1==1:
        # Date Extraction from MercAlicante
        # Options:
        producto='' #Void all products
        familia='' # Void all families
        categoria = '106' # An option of the website: Frutas 

        resp = MercAlicante_scraper(producto, familia, categoria, fecha_inicio)
        # Control Point 
        Save_df_to_csv(resp,'Mercalicante', fecha_inicio[0], str(last_day_Month(fecha_inicio[-1])))
        #file_name_vector.append(resp)
        df = pd.concat([df, resp], ignore_index=True)
        print('Total rows of MercAlicante:', len(resp))
        print('Execution time (min): ', round((time() - start_time)/60, 2))
    if 1==1:
        # Date Extraction from MercaMadrid
        # Options:    
        browser = 'Chrome' # browser name of Selenium
        mercado = 'MERCADO CENTRAL DE FRUTAS'  # An option of the website. 

        resp = MercaMadrid_scraper(browser, mercado, fecha_inicio) 
        # Control Point
        Save_df_to_csv(resp,'MercaMadrid', fecha_inicio[0], str(last_day_Month(fecha_inicio[-1])))
        print('Total rows of MercaMadrid:', len(resp))
        #file_name_vector.append(resp)
        df = pd.concat([df, resp], ignore_index=True)
        print('Execution time (min): ', round((time() - start_time)/60, 2))
    # Unificando datasets
    if 1==1:
        print('Total rows: ', len(df))
        Save_df_to_csv(df,'Mercados Centrales', fecha_inicio[0], str(last_day_Month(fecha_inicio[-1])))
