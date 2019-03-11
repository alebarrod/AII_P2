# P2 para AII por alebarrod

Enunciado de la práctica del Departamento de Lenguajes y Sistemas (LSI) de la Universidad de Sevilla (http://www.lsi.us.es/docencia/pagina_asignatura.php?id=119&cur=2018): "ACCESO INTELIGENTE A LA INFORMACIÓN PRÁCTICA  BEAUTIFULSOUP I Vamos  a  realizar    webscraping,    haciendo    uso    de   BeautifulSoup,    sobre  la  web  de ventas de productos para celíacos:  https://www.ulabox.com/campaign/productos-sin-gluten#gref 
Buscamos construir un programa con Tkinter con tres  botones de opción: 
 - a)“Almacenar Productos”, que sea capaz de extraer y almacenar en una base de datos sqlite  los  productos  sin  gluten.  Para  cada  producto  hay  que  almacenar:  marca, nombre, link a la descripción del producto y precio/s (si está en oferta tiene más de un precio). 
 - b)“Mostrar  Marca”, que  muestre  una  spinbox  que  permita  al  usuario seleccionar  un marca,  extrayéndolas de la BD,  y  muestre  en  otra  ventana  (en  una  listbox  con    scrollbar)    TODOS  los  productos  (nombre,  precio  final)    que  hay  de  dicha marca. 
 - c) “Buscar  Ofertas”,  que  muestre  en  otra  ventana  (en  una  listbox  con  scrollbar)  TODOS  los  productos  en  oferta  (nombre,  precio  sin  oferta,  precio  con  oferta)  que hay."

## Requisitos

Tener instalado Python 3 (el desarrollo se realizó bajo Python 3.6)
Tener instalado BeautifulSoup4: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
Tener instalado el parser para BeautifulSoup4: **html5lib**.

## Ejecución

Para ejecutar la aplicación unicamente debemos abrir una consola e ir al directorio en el que se encuentre scrapApp.py y ejecutar este archivo con Python. La funcionalidad de la aplicación está explicada en el enunciado de la práctica.

## ¡Importante!

El web scraping se basa en aprovechar la estructura de la web para extraer la información publicada en esta de forma automática. Por ello si la web actualiza su estructura el programa no funcionará y tendrá que readaptarse. Para que pueda utilizarse esta aplicación aunque haya cambiado el foro del que se extrae la información podemos adaptar el programa:

- En caso de que se haya dañado alguno de los archivos html copiamos el contenido de la carpeta html (1.html) en el mismo directorio que scrapApp.py.
- Abrimos con un editor de texto scrapApp.py y buscamos la línea: urllib.request.urlretrieve(...,...). La borramos o comentamos.
- Ejecutamos el programa con normalidad. Ahora en lugar de descargar el contenido de la web usará los ficheros html que se encuentren en el directorio.