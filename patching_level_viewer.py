#Se cuencia de codigo que abre el contenido del SRU
from bs4 import BeautifulSoup
import re
with open('test2.htm', 'r') as file:
    raw_SRU = file.read()

#Funcion que toma la lista de parches del sistema y cuenta cuantas veces se repiten dentro del SRU. Devuelve un diccionatio con el parche y su fincionalidad en su key y las veces que se repite como value
def patch_count(list):
    count = {}
    # Iterar sobre cada elemento en la lista
    for element in list:
        # Verificar si el elemento ya está en el diccionario
        if element in count:
            # Si está, incrementar su contador
            count[element] += 1
        else:
            # Si no está, agregarlo al diccionario con contador 1
            count[element] = 1

    return count

def drop_type_cleaning(lista, longitud_minima):
    return [elemento for elemento in lista if len(str(elemento)) <= longitud_minima]


SRU_content = BeautifulSoup(raw_SRU, 'html.parser')
#Se inicializan palabras clave
WS_keyword = re.compile(r'Workstation: ', re.IGNORECASE)
patch_keyword = re.compile(r'OVA3', re.IGNORECASE) 
drop_type_kw_1 = re.compile(r'Operator Station', re.IGNORECASE)
drop_type_kw_2 = re.compile(r'Non-Ovation Drop', re.IGNORECASE)
#Las siguientes lineas se encargan de buscar todos los elementos usando en el tag y la clase apropiadas por medio del keyword
patches = SRU_content.find_all("td", class_="ValueColumn", string=patch_keyword)
workstations = SRU_content.find_all("caption", class_="SectionTitle", string=WS_keyword)
#drop_type = SRU_content.find_all("td", class_="ValueColumn", string=drop_type_kw_1 or drop_type_kw_2)
#drop_type = SRU_content.find_all("td", class_= "ValueColumn", text=lambda text: "Operator Station" in text and "Non-Ovation Drop"  in text )

#drop = drop_type_cleaning(drop_type, len("<td class=\"ValueColumn\">Operator Station</td>"))

patch_list = list()

for line in patches:
    line_split = line.text.split(";")
    patch = line_split[0]
    functionality = line_split[-1].split("Comment:")[-1]
    patch_list.append((patch,functionality))
    patch_list = sorted(patch_list, key=lambda x: x[0])

conteo = patch_count(patch_list)
for patch_number, repetition in conteo.items():
    print(f"Patch: {patch_number}, Repetitions: {repetition}")
    
#print(drop_type.text)
