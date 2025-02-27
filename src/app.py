import os
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

url ='https://companies-market-cap-copy.vercel.app/index.html'

response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

element = soup.find_all("table", limit = 1)[0]

celdas = element.find_all('td')

texto_celdas = [celda.strip() for celda in celdas]

import os
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

#Llamo al URL
url = 'https://companies-market-cap-copy.vercel.app/index.html'
response = requests.get(url)

#Parseo el URL
soup = BeautifulSoup(response.text, "html.parser")

#Busco la primera tabla y posteriormente extraigo las filas
element = soup.find_all("table", limit = 1)[0]
filas = element.find_all('tr')

#Itero sobre cada fila y guardo toda la información en distintas variables
datos_Tesla = []
for fila in filas[1:]:
    filas_valores = fila.find_all("td")
    fecha = filas_valores[0].text.strip()
    ingresos = filas_valores[1].text.strip()
    revenue = filas_valores[2].text.strip()
    datos_Tesla.append([fecha, ingresos,revenue])

#Creo el data frame con los datos guardados en la variable de datos_Tesla
df = pd.DataFrame(datos_Tesla, columns = ['año', 'revenue', 'cambio'])
df = df.sort_values('año')

#Creo una variable para limpiar los datos de revenue y poderlos graficar posteriormente
def limpiar(valor):
    valor = valor.replace("B", "").replace("$", "").replace("%", "").replace(" ", "").strip()
    if valor: 
        return float(valor)
    else: 
        return None  

df_corregido = df['revenue'].apply(limpiar)


#Creo una base de datos y me aseguro que la tabla sólo se cree en caso de no existir porque de lo contrario da error.
con = sqlite3.connect("Ingresos_Tesla.db")

cur = con.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS Ingresos_anuales(
    año TEXT,
    revenue REAL,
    cambio REAL
               
)
""")

df.to_sql('ingresos', con, if_exists='append', index=False)


con.commit()
con.close()

#Primera representación gráfica
plt.figure(figsize=(10, 6))
plt.plot(df["año"], df_corregido, marker='o', label="Ingresos")
plt.title("Ingresos anuales de Tesla")
plt.xlabel("Año")
plt.ylabel("Ingresos en billones de dólares")
plt.legend()


plt.show()

#Segunda representación gráfica
plt.figure(figsize=(10, 6)) 
plt.scatter(df["año"], df_corregido, color='blue', alpha=0.6) 
plt.title('Ingresos anuales de Tesla')
plt.xlabel('Año')
plt.ylabel('Ingresos en billones de dólares')  
plt.show()

#Tercera representación gráfica
plt.figure(figsize=(10, 6))
plt.bar(df["año"], df_corregido, color='blue', alpha=0.7, edgecolor="black")

plt.title('Ingresos anuales de Tesla')
plt.xlabel('Año')
plt.ylabel('Ingresos en billones de dólares')

plt.show()

#Ejercicio extra
df['revenue'] = df_corregido
Beneficios_2024 = df['revenue'].loc[0]
Último_año = df['año'].loc[0]
Beneficios_2024 = int(Beneficios_2024 * 1_000_000 * 1_000_000)

beneficios_finales = f"Tesla ha ganado {Beneficios_2024:,.2f} de dólares en el año {Último_año} ."
print(beneficios_finales)