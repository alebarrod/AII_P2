from bs4 import BeautifulSoup
import tkinter
import sqlite3
import urllib.request
import re

def getAllBrands(dbconnection):
    lista = dbconnection.select()
    listaMarcas = list()
    diccionario = dict()

    for element in lista:
        if element.marca in diccionario:
            diccionario[element.marca].append(element)
        else:
            diccionario[element.marca] = [element]
            listaMarcas.append(element.marca)
    
    return listaMarcas,diccionario

def scrap():
    lista = list()

    #descargar web como '1.html'
    urllib.request.urlretrieve('https://www.ulabox.com/campaign/productos-sin-gluten#gref','1.html')
    html_doc = open('1.html','r', encoding = "utf8")
    #Abrimos usando el parser 'html5lib'
    soup = BeautifulSoup(html_doc, 'html5lib')

    #analizamos cada producto por el tag articulo y por los id que contengan "product"
    for element in soup.find_all('article', id=re.compile("product")):
        
        marca = element['data-product-brand']
        nombre = element['data-product-name']
        precio = float(element['data-price'])   #Lo transformamos a un float
        link = "https://www.ulabox.com" + element.find('a',class_=re.compile("js-article-link"))["href"]
        sale = element.find('del')
        if sale:    #En el caso de que tenga una oferta
            precioAntiguo = float(sale.string.replace(',','.').replace('€','')) #Eliminamos el simbolo de "€" y cambiando la "," por un "."
            lista.append(objectDB(marca, nombre, link, precio, precioAntiguo))
        else:
            lista.append(objectDB(marca, nombre, link, precio))
    
    return lista


        
class DB:
    
    #Crea la base de datos y la tabla que vamos a usar  
    def __init__(self, name = "database.db"):
            self.name = name
            connection = sqlite3.connect(self.name)
            connection.execute('''DROP TABLE IF EXISTS PRODUCTO;''')
            connection.execute('''CREATE TABLE PRODUCTO
                  (ID INTEGER PRIMARY KEY  AUTOINCREMENT NOT NULL,
                  MARCA            TEXT    NOT NULL,
                  NOMBRE           TEXT,
                  LINK             TEXT,
                  PRECIO           REAL,
                  PRECIOANTIGUO    REAL);''')
            connection.close()

    #Insert con todos los parametros
    def insert(self, marca, nombre, link, precio, precioAntiguo):
            connection = sqlite3.connect(self.name)
            if precioAntiguo == None:   #Prepara la sentencia teniendo en cuenta si tiene oferta o no
                template = """INSERT INTO PRODUCTO (MARCA, NOMBRE, LINK, PRECIO) VALUES ("{marca}","{nombre}","{link}",{precio});"""
                formatted_string = template.format(marca = marca, nombre = nombre, link = link, precio = precio)
            else:
                template = """INSERT INTO PRODUCTO (MARCA, NOMBRE, LINK, PRECIO, PRECIOANTIGUO) VALUES ("{marca}","{nombre}","{link}",{precio},{precioAntiguo});"""
                formatted_string = template.format(marca = marca, nombre = nombre, link = link, precio = precio, precioAntiguo = precioAntiguo)
            connection.execute(formatted_string);
            connection.commit()
            connection.close()

    #Select todos los objetos. Devuelve una lista con todos los objetos
    def select(self):
            lista = list()
            connection = sqlite3.connect(self.name)
            res = connection.execute("""SELECT * FROM PRODUCTO;""")
            for obj in res:
                  lista.append(objectDB(obj[1],obj[2],obj[3],obj[4],obj[5]))
            connection.close()
            return lista        

    #Devuelve los productos que tienen oferta
    def selectOfertas(self):
            lista = list()
            connection = sqlite3.connect(self.name)
            res = connection.execute("""SELECT * FROM PRODUCTO WHERE PRECIOANTIGUO IS NOT NULL;""")
            for obj in res:
                  lista.append(objectDB(obj[1],obj[2],obj[3],obj[4],obj[5]))
            connection.close()
            return lista


class objectDB():
    def __init__(self, marca, nombre, link, precio, precioAntiguo = None):
        self.marca = marca
        self.nombre = nombre
        self.link = link
        self.precio = precio
        self.precioAntiguo = precioAntiguo

    def toString(self):
        if self.precioAntiguo == None:
            res = 'Marca: ' + self.marca + '. Producto: ' + self.nombre + ' (' + self.link + '). Precio: ' + str(self.precio) + '.'
        else:
            res = 'Marca: ' + self.marca + '. Producto: ' + self.nombre + ' (' + self.link + '). Precio: ' + str(self.precio) + '. Precio original: ' + str(self.precioAntiguo) + '.'
        return res

class App:
    def __init__(self):
        #Creacion de base de datos
        self.dbconnection = DB("practica1.db")

        #Creación de aplicación de escritorio
        self.app = tkinter.Tk()

        #Main menu options
        self.button1 = tkinter.Button(self.app, text = "Almacenar Productos", command = self.almacenarProductos).grid(row = 0, column = 0)
        self.button2 = tkinter.Button(self.app, text = "Mostrar Marca", command = self.mostrarMarca).grid(row = 0, column = 1)
        self.button3 = tkinter.Button(self.app, text = "Buscar Ofertas", command = self.buscarOfertas).grid(row = 0, column = 2)

        self.app.mainloop()
    
    def almacenarProductos(self):
        lista = scrap() #Hacer scrap y devolver una lista con los objetos para la base de datos
        for element in lista:
            #almacenar objetos
            self.dbconnection.insert(element.marca, element.nombre, element.link, element.precio, element.precioAntiguo)

    
    def mostrarMarca(self):
        #Create new window
        self.ventanaMarca = tkinter.Tk()
        tuplaMarcas,diccionarioMarcas = getAllBrands(self.dbconnection) #Devuelve una tupla con las marcas y un diccionario con los productos ordenados por marca (key)

        #Crear spinbox con las marcas
        spinbox = tkinter.Spinbox(self.ventanaMarca, values = tuplaMarcas)
        spinbox.grid(row = 0)

        #Mostrar los productos por marca
        button = tkinter.Button(self.ventanaMarca, text = "Buscar", command = lambda: self.productosMarca(spinbox.get(), diccionarioMarcas)).grid(row = 1, column = 0)
        

        #Run loop
        self.ventanaMarca.mainloop()

    def productosMarca(self, marca, diccionarioMarcas):
        #Crear ventana
        self.ventanaMarca2 = tkinter.Tk()

        #Añadimos un scrollbar vertical
        scrollbar = tkinter.Scrollbar(self.ventanaMarca2)
        scrollbar.pack(side = "right", fill= "y")

        ListboxMarcas = tkinter.Listbox(self.ventanaMarca2, width = 200, height = 30, yscrollcommand = scrollbar.set)

        i = 1
        for element in diccionarioMarcas[marca]:
            ListboxMarcas.insert(i, element.toString())
            i = i + 1

        ListboxMarcas.pack()

        self.ventanaMarca2.mainloop()

    def buscarOfertas(self):
        self.ventanaOfertas = tkinter.Tk()
        #Añadimos un scrollbar vertical
        scrollbar = tkinter.Scrollbar(self.ventanaOfertas)
        scrollbar.pack(side = "right", fill= "y")

        #Create list box
        ListboxOfertas = tkinter.Listbox(self.ventanaOfertas, width = 200, height = 30, yscrollcommand = scrollbar.set)
        
        consulta = self.dbconnection.selectOfertas()

        i = 1
        for element in consulta:
            ListboxOfertas.insert(i, element.toString())
            i = i + 1
        ListboxOfertas.pack()

        self.ventanaOfertas.mainloop()

App()