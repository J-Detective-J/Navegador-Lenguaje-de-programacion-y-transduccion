# Navegador - Lenguaje de programacion y transduccion
Programa que simula un navegador, utilizando las funciones de navegación, autocompletar y "recomendación de productos"

## Problema 1: Sistema de navegación de páginas web
Cree un diagrama de flujo o diagrama que ilustre cómo funcionará la navegación.

<img width="747" height="960" alt="diagrama_navegador_busqueda" src="https://github.com/user-attachments/assets/5b8f9048-5261-4087-a3d8-df6a67b2e0db" />

## Métodos para la Navegación
### Defina los métodos que necesitará
- search(query=None)  ------- Propósito: Realiza una nueva búsqueda
- navigate(direction) ------- Propósito: Navega en el historial (atrás/adelante)
- load_results(query) ------- Propósito: Carga y muestra resultados de búsqueda
- update_entry(query) ------- Propósito: Sincroniza barra de búsqueda con consulta actual



## Problema 2: Función de autocompletar
Cree un diagrama que ilustre cómo se estructurará el diseño.

<img width="1079" height="860" alt="diagrama_autocompletar" src="https://github.com/user-attachments/assets/636fba2d-f8cc-4fd1-be16-d765f23f198c" />


## Métodos para la Autocompletar
### Defina los métodos que necesitará
- load_results(query) ------- Propósito: Obtiene resultados de búsqueda principales
- autocomplete(event) ------- Propósito: Obtiene sugerencias mientras el usuario escribe
- show_recommendations() ---- Propósito: Obtiene temas relacionados (simula "también compraron")
- load_results() ------------ Procesamiento de JSON

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Instrucciones de uso:
- Debes tener python 3 (como minimo)
  
### ¿Como instalar python?
### Windows
Ve a la página oficial: https://www.python.org/downloads/
<br>
Descarga la última versión estable para Windows

### Linux
1. Actualizar repositorios: <br>
```sudo apt update```
2. Instalar Python :<br>
```sudo apt install python3 python3-pip```

### Instalar librerias
### Windows
```pip install requests```<br>
o<br>
```python -m pip install requests```<br>

### Linux

```pip3 install requests```

Luego instalar Tkinter

```sudo apt install python3-tk```

### Para ejecutar el .py debes ubicarte en la carpeta, abrir el terminal/cmd y ejecutar el siguente comando
### Windows
<br>```python buscador.py```<br>
o
<br>```python3 buscador.py```
### Linux
<br>```python3 buscador.py```
