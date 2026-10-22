# Visualizador de Red de Coocurrencia de Palabras Clave (RSL)

Aplicación de escritorio desarrollada en Python con **Tkinter** para automatizar el análisis bibliométrico de palabras clave en Revisiones Sistemáticas de la Literatura (RSL). Permite cargar datos desde archivos Excel (`.xlsx`), construir grafos de coocurrencia entre términos y exportar la visualización en alta calidad.

---

## 📋 Estructura y Formato del Archivo Excel (`.xlsx`)

Para que la aplicación lea los datos correctamente, el archivo Excel debe cumplir con las siguientes especificaciones:

* **Columna principal:** La primera columna de la hoja debe contener la lista de palabras clave extraídas de cada artículo.
* **Separador:** Las palabras clave dentro de cada celda deben estar separadas explícitamente por punto y coma (`;`).
* **Formatos admitidos:** Archivos con extensión `.xlsx`.

### Ejemplo de entrada de formato Excel:
| Keywords |
| :-------------------------------------------------------------- |
| artificial intelligence; iot; smart irrigation; sensor networks |
| precision agriculture; iot; fertilization; machine learning |
| smart irrigation; water management; sensor networks; ai |

---

## 🛠️ Librerías Utilizadas

El proyecto utiliza la pila estándar de procesamiento de datos y grafos en Python:

* **`pandas`**: Lectura y filtrado del archivo `.xlsx`.
* **`networkx`**: Construcción del grafo, cálculo de pesos por coocurrencia y algoritmos de distribución de nodos (`spring_layout`).
* **`matplotlib`**: Renderizado de la red neuronal/mapa conceptual y exportación gráfica.
* **`openpyxl`**: Motor interno necesario para que Pandas procese archivos de Excel modernos.
* **`tkinter`** *(incluido en Python)*: Construcción de la interfaz gráfica de usuario (GUI).

---

## 📦 Instalación de Dependencias

Ejecuta el siguiente comando en tu terminal o símbolo del sistema (`cmd`) para instalar las librerías necesarias:

```bash
pip install pandas networkx matplotlib openpyxl
```
## Ejecución y modo de uso
Se puede contar con entornos de desarrollo integrado (IDE) como Visual Studio Code, PyCharm, ThonnyPython para la ejecucion del programa o optar una ejecución directa desde la consola de comandos (CMD) mediante la ruta exacta donde se ubica el archivo.
--> C:\Users\Person> python GraficosRSL.py

Interfaz: Selecciona el archivo Excel, modificar dinámicamente el parametro de cantidad de palabras clave y exportar el grafico en formatos PNG, JPEG y PDF.

