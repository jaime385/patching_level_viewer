#Se cuencia de codigo que abre el contenido del SRU
from bs4 import BeautifulSoup
import re
import pandas as pd
filename = input('Enter the path of the file X:\...\SysRegReport.htm : ')
with open(filename, 'r') as file:
    raw_SRU = file.read()
    
    
def delete_duplicates(lista):
    # Convertir la lista de tuplas a un conjunto de tuplas para eliminar duplicados
    temp_set = set(lista)

    # Convertir de nuevo el conjunto a una lista de pares ordenados
    list_without_duplicates = list(temp_set)

    return list_without_duplicates

#Se llama a la libreria importada para poder parsear el contenido el archivo html    
SRU_content = BeautifulSoup(raw_SRU, 'html.parser')
#Inicializacion de palabras clave
WS_keyword = re.compile(r'Workstation: ', re.IGNORECASE)
ova_patch_keyword = re.compile(r'OVA3', re.IGNORECASE)
oph_patch_keyword = re.compile(r'OPH3', re.IGNORECASE)   
#Las siguientes lineas se encargan de buscar todos los elementos usando el tag y la clase apropiadas por medio del keyword
workstations_in_SRU = SRU_content.find_all("caption", class_="SectionTitle", string=WS_keyword)
#Lista que contiene todos los nombres de las workstations
ws_list = list()
#Ciclo que guarda todos los nombres de las Workstations en la lista anterior
for machine in workstations_in_SRU:
    ws_list.append(machine.text.strip())

#Dentro de la siguiente variable/lista se encuentran los tags que contienen toda la info de las WS pero debe limpiarse
table_ST = (SRU_content.find_all("table", class_= "SectionTable")) 

#La siguiente lista va a contener las porciones de codigo html cuyo header va a ser el nombre de la WS
ws_info = list()

#El siguiente ciclo se encarga de barrer sobre los headers comparando el header con todos los elementos de la lista de nombres de maquinas y guardando las porciones de codigo html cuyo header coincida con el nombre de alguna maquina
for i in range(0,len(table_ST)):
    for ws in ws_list:
        if ws == table_ST[i].find("caption", class_="SectionTitle").text.strip():
            ws_info.append(table_ST[i])
        else:
            pass

#El siguiente diccionario va a tener como key o llave el nombre del drop y como value una lista con todos los parches
ws_patch_level = {}
#La siguiente lista sera una lista cuyos elementos seran pares ordenados donde la primera coordenada es el parche y la segunda su descripcion
patches_and_descriptions = []

#El siguiente ciclo se encarga de tomar y separar la informacion obtenida en la lista ws_info y extraer los nombres de las maquinas con sus respectivos parches y llenar el diccionario definido anteriormente
for j in range(0, len(ws_info)):
    ws_ova_patches = ws_info[j].find_all("td", class_="ValueColumn", string = ova_patch_keyword) #Lista que va a contener la info de los parches de Ovation tomada del html, los elementos de esta lista deben limpiarse
    ws_oph_patches = ws_info[j].find_all("td", class_="ValueColumn", string = oph_patch_keyword) ##Lista que va a contener la info de los parches de OPH tomada del html, los elementos de esta lista deben limpiarse
    drop = (ws_info[j].find("caption", class_="SectionTitle").text.strip()).replace("Workstation: ","")#Variable que va a contener el nombre del drop, las funciones strip y replace se encargan de devolver unicamente el nombre del drop
    ws_ova_patches_list = list() #Lista que va a contener los parches de Ovation del j-esimo elemento de ws_info. En cada ciclo la lista se limpia
    ws_oph_patches_list = list() #Lista que va a contener los parches de OPH del j-esimo elemento de ws_inf. En cada ciclo la lista se limpia
 
    for line1 in ws_ova_patches:
        #Se toma la linea de texto y se separa con base en el caracter ;
        line_split1 = line1.text.split(";")
        patch1 = line_split1[0] #El primer elemento de la linea es el que contiene el nombre del parche
        ws_ova_patches_list.append(patch1) #Se guarda el parche en la lista
        functionality1 = line_split1[-1].split("Comment:")[-1].replace("\n                  ", " ").strip() #Esta linea toma el comment o funcionalidad del parche y lo guarda en la variavle functionality1
        patches_and_descriptions.append((patch1,functionality1)) #Se guarda el parche y su funcionalidad en forma de par ordenado en la patches_and_descriptions
    ws_ova_patches_list = sorted(ws_ova_patches_list)# Se ordenan los elementos de la lista con base en el nombre del parche

    for line2 in ws_oph_patches:
        #Se toma la linea de texto y se separa con base en ;
        line_split2 = line2.text.split(";")
        patch2 = line_split2[0] #El primer elemento de la linea es el que contiene el nombre del parche
        ws_oph_patches_list.append(patch2) #Se guarda el parche en la lista
        functionality2 = line_split2[-1].split("Comment:")[-1].replace("\n                  ", " ").strip()  #Esta linea toma el comment o funcionalidad del parche y lo guarda en la variavle functionality2
        patches_and_descriptions.append((patch2,functionality2)) #Se guarda el parche y su funcionalidad en forma de par ordenado en la lista patch_list
    ws_oph_patches_list = sorted(ws_oph_patches_list)# Se ordenan los elementos de la lista con base en el nombre del parche
    #La siguiente linea mezcla las dos listas y la siguiente asigna el nombre del drop como key y la lista como value del diccionario
    all_ws_patches = ws_ova_patches_list + ws_oph_patches_list
    ws_patch_level[drop] = all_ws_patches

#Se eliminan los duplicados de la lista patches and descriptions
patches_and_descriptions = delete_duplicates(patches_and_descriptions)
#La siguiente linea lo que hace es tomar la longitud maxima de las filas del dataframe que debe crearse mas adelante
len_max = max(len(lst) for lst in ws_patch_level.values())

# Rellena las listas más cortas con tuplas vacías para que tengan la misma longitud
for key, value in ws_patch_level.items():
    if len(value) < len_max:
        ws_patch_level[key].extend(["-"] * (len_max - len(value)))

# Crea el DataFrame a partir del diccionario
ws_patch_level_df = pd.DataFrame(ws_patch_level)
patches_and_descriptions_df = pd.DataFrame(patches_and_descriptions, columns=["Patch", "Description"])
#A continuacion se convierten los dataframes creados anteriormente en hojas de excel
with pd.ExcelWriter("Patch level review.xlsx", engine='xlsxwriter') as writer:
    ws_patch_level_df.to_excel(writer, sheet_name='Patch level', index=False)
    patches_and_descriptions_df.to_excel(writer, sheet_name='Patches and descriptions', index=False)







