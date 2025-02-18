# EJEMPLO DE LA INTEGRACIÓN DE UN CHATBOT 
En este repositorio, se van a poder encontrar 2 carpetas:
1. La carpeta del frontend (fronted-chatbot)
2. La API para generar las respuestas del modelo.

## HERRAMIENTAS NECESARIAS PARA SU EJECUCIÓN
### FRONTEND
En la parte del frontend, se ha utilizado React, con el empaquetador Vite. Por ello, es necesario tener instalado con anterioridad, o es recomendable, Node.js y Vite. 
Para ejecutar el proyecto del frontend, se deben de seguir los siguientes comandos, que se ejecutaran dentro de la carpeta "frontend-chatbot":
1. Descargar todas las dependencias.
```bash
npm install
```

2. Para ejecutar el proyecto:
```bash
npm run dev
```

### BACKEND
En la parte de la API, se ha utilizado Flask con Python. Para poder ejecutar la API sin problemas, es necesario seguir los siguientes pasos:
1. Tener instalado con anterioridad Python y su correspondiente gestor de paquetes "pip"
2. Descargar las dependencias. El siguiente comando se debe de realizar en el directorio donde se encuentre el archivo "requirements.txt". Es decir, "Servers/python/flask":
```bash
pip install -r requirements.txt
```
3. Finalmente, ejecutar el siguiente comando en la carpeta donde se encuentra el archivo principal "app.py":

```bash
py app.py
```
