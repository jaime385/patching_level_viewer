#Se cuencia de codigo que abre el contenido del SRU
from bs4 import BeautifulSoup
import re
with open('test2.htm', 'r') as file:
    raw_SRU = file.read()

#Se llama a la libreria importada para poder parsear el contenido el archivo html    
SRU_content = BeautifulSoup(raw_SRU, 'html.parser')
#Inicializacion de palabras clave
WS_keyword = re.compile(r'Workstation: ', re.IGNORECASE)
#Las siguientes lineas se encargan de buscar todos los elementos usando en el tag y la clase apropiadas por medio del keyword
workstations_in_SRU = SRU_content.find_all("caption", class_="SectionTitle", string=WS_keyword)
#Lista que contiene todos los nombres de las workstations
ws_list = list()
#Ciclo que guarda todos los nombres de las Workstations en la lista anterior
for machine in workstations_in_SRU:
    ws_list.append(machine.text.strip())

#Dentro de la siguiente variable/lista se encuentran los tags que contienen toda la info de las WS pero debe limpiarse
table_ST = (SRU_content.find_all("table", class_= "SectionTable")) 

#dummy_var = table_ST[0].find("caption", class_="SectionTitle").text.strip() #Esta variable la hice para probar si podia obtener
#La siguiente lista va a contener las porciones de codigo html cuyo header va a ser el nombre de la WS
ws_info = list()

#El siguiente ciclo se encarga de barrer sobre los headers comparando el header con todos los elementos de la lista de nombres de maquinas y guardando las porciones de codigo html cuyo header coincida con el nombre de alguna maquina
for i in range(0,len(table_ST)):
    for ws in ws_list:
        if ws == table_ST[i].find("caption", class_="SectionTitle").text.strip():
            ws_info.append(table_ST[i])
        else:
            pass
        
print(ws_info[1])


