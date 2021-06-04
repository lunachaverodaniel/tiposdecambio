import sys
import pandas as pd
import requests
import json
from datetime import date, timedelta,datetime
from typing import List
from bs4 import BeautifulSoup as bs



def descargaHTML(url):
    """Ésta funcion descarga el HTML crudo de alguna URL específica

    - **parameters**, **types**, **return** and **return types**::

          :param url: URL con los querystrings del token y las monedas a obtener
          :type url: string
          :return: Regresa un objeto con el HTML de la pagina.
          :rtype: Retorna una cadena

    """
    response = requests.get(url)
    return response.content

def getRawExchangeDOF(url):
    '''
    Esta función realiza el webscraping de una URL definida por el Diario Oficial de la Federación
    Parámetros
    @parametro 1 (url): url que va a consumir el servicio
    '''
    try:
        df = pd.DataFrame()
        rawExchanges = bs(descargaHTML(url),'html.parser')
        estructura = rawExchanges.find_all(class_="Celda 1")
        #data = []
        for elem in estructura:
            vals = bs(str(elem),'html.parser')
            monedas = vals.find_all('td')
            df_row={
                'fecha': datetime.strptime(str(monedas[0].text),'%d-%m-%Y').strftime('%d/%m/%Y'),
                'dato' : float(monedas[1].text)
            }
            df = df.append(df_row,ignore_index=True)
        df = df.set_index('fecha')

    except:
        print("Ocurrió un error!",sys.exc_info()[0],"occured.")
        return 0
    return df
    
def obtenerDOF():
    '''
    Esta función arma la URL e invoca el servicio de webscraping
    '''
    fecha = date.today().strftime('%d/%m/%Y')
    url = "https://dof.gob.mx/indicadores_detalle.php?cod_tipo_indicador=158&dfecha={}&hfecha={}".format(fecha,fecha)
    response = getRawExchangeDOF(url)
    return response

def obtenerDOFPorRango(fec_inicio, fec_fin):
    '''
    Esta función arma la URL del servicio de webscraping utilizando un rango de fechas
    @parametro 1 (fec_inicio): fecha inicial del rango
    @parametro 2 (fec_fin): fecha final del rango
    '''
    fec_ini = datetime.strptime(fec_inicio,'%d/%m/%Y').strftime('%d/%m/%Y')
    fec_fin = datetime.strptime(fec_fin,'%d/%m/%Y').strftime('%d/%m/%Y')
    url = "https://dof.gob.mx/indicadores_detalle.php?cod_tipo_indicador=158&dfecha={}&hfecha={}".format(fec_ini,fec_fin)
    response = getRawExchangeDOF(url)
    #print(response)
    return response

def obtenerinformacionBANXICO(series,token):
    '''
    Esta función obtiene la información del servicio SIE de las series de tiempo de monedas proporcionado por el BANXICO 
    @parametro 1 (series): Las series separadas por , a obtener ej: 'SF4605,SF46410'
    @parametro 2 (token): Token de acceso proporcionado por BANXICO
    '''
    api_url_base = "https://www.banxico.org.mx/SieAPIRest/service/v1/series/:idSeries/datos/oportuno"
    api_url_base = api_url_base.replace(':idSeries',series)
    api_token = token
    url = "{}?token={}".format(api_url_base,api_token)

    headrs={'Content-Type':'application/json'}
    response = requests.get(url,headers=headrs)

    if (response.status_code == 200):
        json_data = json.loads(response.content)
        df = pd.DataFrame()

        for serie in json_data['bmx']['series']:
            df_row = {'serie': serie['idSerie'],
                      'fecha': serie['datos'][0]['fecha'],
                      'dato' : float(serie['datos'][0]['dato'])
                    }
            df = df.append(df_row, ignore_index=True) 
        df = df.pivot_table(index='fecha',columns='serie',values='dato')
        return df
    else:
        print("Hubo un error")
        return 0

def obtenerinformacionBANXICORango(series,token,fechaInicial,fechaFinal):
    '''
    Esta función obtiene la información del servicio SIE proporcionado por el BANXICO de las series determinadas en un periodo o rango de fechas específico
    @parametro 1 (series): Las series separadas por , a obtener ej: 'SF4605,SF46410'
    @parametro 2 (token): Token de acceso proporcionado por BANXICO
    @parametro 3 (fechaInicial): Fecha inicial.
    @parametro 4 (fechaFinal): Fecha final del rango.
    '''
    api_url_base = "https://www.banxico.org.mx/SieAPIRest/service/v1/series/:idSeries/datos/:fechaInicial/:fechaFinal"
    api_url_base = api_url_base.replace(':idSeries',series)
    api_url_base = api_url_base.replace(':fechaInicial',datetime.strptime(fechaInicial,'%d/%m/%Y').strftime('%Y-%m-%d'))
    api_url_base = api_url_base.replace(':fechaFinal', datetime.strptime(fechaFinal,'%d/%m/%Y').strftime('%Y-%m-%d'))
    api_token = token
    url = "{}?token={}".format(api_url_base,api_token)

    headrs={'Content-Type':'application/json'}
    response = requests.get(url,headers=headrs)

    if (response.status_code == 200):
        json_data = json.loads(response.content)
        df = pd.DataFrame()

        for serie in json_data['bmx']['series']:
            for item in serie['datos']:
                df_row = {'serie': serie['idSerie'],
                      'fecha': item['fecha'],
                      'dato' : float(item['dato'])
                    }
                df = df.append(df_row, ignore_index=True)
        df = df.pivot_table(index='fecha',columns='serie',values='dato')
        return df
    else:
        print("Ocurrió un error!",sys.exc_info()[0],"occured.")
        return 0

def main():
    
    series = sys.argv[1]
    token = sys.argv[2]
    salida = sys.argv[3]
    if len(sys.argv) > 4: # Si esta condición se cumple entonces la actualización es del día corriente:
        fechaInicial = sys.argv[4]
        fechaFinal = sys.argv[5]
        dofrango = obtenerDOFPorRango(fechaInicial,fechaFinal)
        banxicoRango = obtenerinformacionBANXICORango(series,token,fechaInicial,fechaFinal)
        df_final = pd.concat([dofrango,banxicoRango], axis = 1, sort=True, ignore_index=True)
        df_final.to_csv(salida, mode='a',header=False)
    else :
        dof = obtenerDOF()
        banxico = obtenerinformacionBANXICO(series,token)
        df_final = pd.concat([dof,banxico], axis = 1, sort=False, ignore_index=True)
        
    
if __name__== "__main__":
    main()
    



