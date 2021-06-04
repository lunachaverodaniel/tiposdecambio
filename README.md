# Monedas de Tipo de Cambio

Este es un proyecto desarrollado en Python cuya finalidad es obtener información de tipos de cambio publicados/proporcionados por las siguientes fuentes:

-   Diario Oficial de la Federación (Tipos de cambio y tasas)

-   Banco de México (Servicio de Información Económica)

Actualmente estas series de tiempo pueden ser obtenidas utilizando un rango histórico de información, también es posible obtener la información diaria de los tipos de cambio.

Este script está parametrizado para obtener forzosamente la información del Dólar del sitio DOF y a su vez un listado indicado en los parámetros de las series que se desean obtener.

Lo anterior quiere decir que el script se parametrizó para obtener una, o varias series de tiempo, ej. Dólar Americano, Euros, Reales, Peso Argentino, Rupias,etc.

A continuación se muestra un ejemplo de llamada del script para obtener el valor actual de la moneda:
Los parámetros solicitados son:

1.  Series Banxico a obtener. Estas series se separan por comas y se encierran entre paréntesis simples.

2.  Token de autenticación. Token proporcionado por BANXICO para acceso al SIE (Sistema de Información Económica).

3.  Archivo de salida. Nombre del archivo donde se guardará la información.

```sh
python .\actualizatipocambio.py 'SF46405,SF46410' 'cfebce03dce48c84ca9df09e3127569c1214623c894eeb48855bf68675ace8a2' './tipodecambio.csv'
```

A continuación se muestra un ejemplo para obtener información histórica de las monedas especificadas en un rango de fechas. Los parámetros a enviar son:

1.  Series Banxico a obtener. Estas series se separan por comas y se encierran entre paréntesis simples.

2.  Token de autenticación. Token proporcionado por BANXICO para acceso al SIE (Sistema de Información Económica).

3.  Archivo de salida. Nombre del archivo donde se guardará la información.

4.  Fecha inicial. Rango inicial que obtendrá la información de las monedas. Se especifíca en el siguiente formato: __'dd/mm/YYYY'__

5.  Fecha final. Rango final que obtendrá la información de las monedas. Se especifíca en el siguiente formato: __'dd/mm/YYYY'__

```sh
python .\actualizatipocambio.py 'SF46405,SF46410' 'cfebce03dce48c84ca9df09e3127569c1214623c894eeb48855bf68675ace8a2' './tipodecambiohistorico.csv' '01/01/2015' '02/12/2019'
```