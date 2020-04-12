# Tipología y ciclo de vida de los datos: Práctica 1

## Descripción

El objetivo de esta práctica es la aplicación de distintas técnicas de extracción de datos para la generación de un _dataset_ que será utilizado más adelante con fines analíticos. 

El conjunto de datos generado contiene los precios mensuales de varias materias primas obtenidas de mercados mayoristas y fabricantes, así como precios agregados e índices de precios (generales y agrícolas) con periodicidad igual o menor (trimestral y anual). Algunas de las variables incluyen el mes y año, el nombre del producto y su precio en euros. El rango temporal se sitúa entre los años 2017 y 2019, ambos incluidos, aunque no se dispone de todos los datos en esos tres años.

Los orígenes de datos utilizados han sido:
* **Federación Española de Industriales Fabricantes de Aceite de Oliva** (http://www.infaoliva.com)
* **Mercados Centrales de Abastecimientos de Alicante, S.A. (Mercalicante)** (https://www.mercalicante.com)
* **Mercados Centrales de Abastecimientos de Madrid, S.A. (Mercamadrid)** (https://www.mercamadrid.es)
* **Eurostat (Oficina de estadística de la Unión Europea)** (https://ec.europa.eu/eurostat/)


[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3749020.svg)](https://doi.org/10.5281/zenodo.3749020)

## Miembros del equipo

La práctica ha sido realizada por **Jesús González Leal** y **Francisco Enrique Lorente Banegas**.

## Ficheros del código fuente

* **src/Scraping_All.py**: punto de entrada. Llama a los distintos métodos de extracción de datos (_web scraping_, API) para los orígenes elegidos y los une en el dataset final _Eurostat_Infaoliva_MercadosCentrales_20170101_20191231.csv_.
* **src/Scraping_MercaAlicante.py**: contiene la implementación de los métodos que extraen datos de la web de Mercalicante y generan el dataset correspondiente.
* **src/Scraping_MercaMadrid.py**: contiene la implementación de los métodos que extraen datos de la web de Mercamadrid y generan el dataset correspondiente.
* **src/genera_dataset_eurostat_infaoliva.py**: llama a los métodos implementados en **scraper_aceite.py** y **api_eurostat.py** y une los resultados en un único dataset.
* **src/scraper_aceite.py**: contiene la implementación de los métodos que extraen datos de la web de Infaoliva y generan el dataset correspondiente.
* **src/api_eurostat.py**: contiene la implementación de los métodos que extraen datos de las estadísticas seleccionadas de Eurostat y generan el dataset correspondiente.
* **src/tools.py**: contiene la implementación de distintos métodos útiles para el conjunto del código.

## Ficheros adicionales
* **csv/Eurostat_Infaoliva_MercadosCentrales_20170101_20191231.csv**: es el dataset final generado.
* **pdf/PRA1.pdf**: contiene las respuestas de la práctica.


## Recursos
1. Subirats, L., Calvo, M. (2018). _Web Scraping_. Editorial UOC.
2. Lawson, R. (2015). _Web Scraping with Python_. Packt Publishing Ltd. Chapter 2. Scraping the Data.
