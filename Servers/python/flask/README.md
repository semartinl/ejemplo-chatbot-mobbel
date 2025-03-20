## !AVISOS IMPORTANTES!
Si vas a utilizarlo en local, se necesita que se tenga instalado en el sistema `ollama`, un framework de Meta para cargar modelos en local. Para instalarlo, pincha en el siguiente enlace para descargarlo. [Ollama link](https://ollama.com/download) 

Si deseas utilizar un Docker para ejecutar dicho framework, es necesario que se sigan las instrucciones para levantar el sistema mediante Dockers. Estas instrucciones se encuentran dentro de la carpeta raiz del proyecto. Se ha implementado un `docker-compose.yml` para realizar correctamente el despliegue sin problemas.

![Deep Chat](../../../assets/readme/flask-connect.png)

This is an example Flask server template that can be used to communicate with the [Deep Chat](https://www.npmjs.com/package/deep-chat) component. It includes a variety of endpoints that can be used to host your own service or act as a proxy for the following AI APIs - [OpenAI](https://openai.com/blog/openai-api), [HuggingFace](https://huggingface.co/docs/api-inference/index), [StabilityAI](https://stability.ai/), [Cohere](https://docs.cohere.com/docs).

### :calling: UI component

This project is preconfigured to work with the example [UI project](https://github.com/OvidijusParsiunas/deep-chat/tree/main/example-servers/ui). Once both are running - they should be able to communicate with each other right out of the box.

### :computer: Local setup

If you are downloading the project via `git clone` - we advise you to use shallow cloning with the use of the [--depth 1](https://www.perforce.com/blog/vcs/git-beyond-basics-using-shallow-clones) option to reduce its size:

```
git clone --depth 1 https://github.com/OvidijusParsiunas/deep-chat.git
```

Navigate to the `src` directory and run the following command to install the required packages:

```
pip install flask flask-cors load_dotenv
pip install -r requirements.txt
```

Run the project:

```
python app.py
```

If you want to use the proxies, please create an `.env` file and define the corresponding environment variables. E.g. if you want to use OpenAI API, define the `OPENAI_API_KEY` variable. See the `.env.example` file.

### :wrench: Improvements

If you are experiencing issues with this project or have suggestions on how to improve it, do not hesitate to create a new ticket in [Github issues](https://github.com/OvidijusParsiunas/deep-chat/issues) and we will look into it as soon as possible.
