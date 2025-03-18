# EJEMPLO DE LA INTEGRACIÓN DE UN CHATBOT 
En este repositorio, se van a poder encontrar 2 carpetas:
1. La carpeta del frontend (fronted-chatbot)
2. La API para generar las respuestas del modelo.

## EJECUCIÓN 
### ANTES DE EJECUTAR
Antes que nada, es necesario que se modifique el docker compose, en el apartado de environment, del servicios de la API para que sea capaz de hacer las llamadas correspondientes a la API de Hugging Face. Para ello, se deberá de cambiar la propieadad de environment siguiente por vuestra correspondiente API key de HF:
```yml
environment:
      - HUGGING_FACE_API_KEY="tu-api-key"
```
### PARA EMPEZAR LA EJECUCIÓN
Se ha establecido un Docker para ambos apartados, tanto para la API como para el diseño web. Para ejecutarlo todo, en la carpeta raiz, ejecuta el siguiente comando:
```bash
docker-compose build
docker-compose up
```
1. El primer comando se utiliza para preparar el entorno de ambos Dockers y sus respectivas imagenes.
2. Se utiliza para desplegar ambos contenedores

### PARA PARAR LA EJECUCIÓN
Si lo que quieres es bajar el despliegue, utiliza el siguiente comando en la misma carpeta donde has realizado los anteriores comandos:
```bash
docker-compose down
```
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


# CUIDADO
En la parte del backend, sobre todo en la API de Mongo, es necesario descargar una libreria llamada "poppler" para poder leer los PDF. Para ello, es necesario descargar el archivo de su correspondiente repositorio de Github. 