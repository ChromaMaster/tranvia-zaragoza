# Tranvia Zaragoza - Telegram Bot

Bot de telegram que indica a los usuarios los tiempos de llegada de los tranvías
de zaragoza a las distintas paradas

## Tabla de contenidos

- [Tranvia Zaragoza - Telegram Bot](#tranvia-zaragoza---telegram-bot)
    - [Tabla de contenidos](#tabla-de-contenidos)
    - [Comenzando](#comenzando)
        - [Requisitos](#requisitos)
        - [Instalacion](#instalacion)
        - [Usando Docker](#usando-docker)
    - [License](#license)

## Comenzando

Para poder utilizar puedes descargarlo utilizando lo siguiente

```sh
git clone https://gitlab.unizar.es/pulsar/tranvia-zaragoza.git
cd tranvia-zaragoza
```

Sigue los pasos mostrados abajo para instalar los **Requisitos** y para la **Instalacion**

**[Volver arriba](#tabla-de-contenidos)**

### Requisitos

Este proyecto esta implementado haciendo uso de la herramienta
[Pipenv](https://docs.pipenv.org/) la cual ayuda al encapsulamiento del proyecto.

Para poder hacer uso de esto hará falta instalarlo en tu sistema. Una vez instalado
las demás dependencias estan definidas en el fichero [Pipfile](Pipfile). Para
instalarlas, simplemente ejecuta el comando `pipenv install`

- [Python Telegram Bot](https://github.com/python-telegram-bot/python-telegram-bot)
- [Requests](http://docs.python-requests.org/en/master/)
- [PyYAML](http://pyyaml.org/wiki/PyYAMLDocumentation)

**[Volver arriba](#tabla-de-contenidos)**

### Instalacion

Para iniciar el bot, lo primero que hace falta es definir la configuración
de este. Para ello, dentro del fichero `etc/config.yaml` se debe poner el token 
del bot obtenido del (BotFather)[https://telegram.me/BotFather].

```
---
app:
  token: "<TU_TOKEN_AQUI>"
```

Una vez realizado esto, se puede ejecutar el bot desde el **virtualenv**.
Para acceder a este, una vez en el mismo directorio del proyecto se ejecuta
`pipenv shell` y a continuación `python3 main.py`.

**[Volver arriba](#tabla-de-contenidos)**

### Usando Docker

Para desplegar este bot utilizando Docker puedes seguir los siguientes pasos.

- Constryue la imagen utilizando el [Dockerfile](Dockerfile) proporcionado

```sh
docker build -t <nombre_de_la_imagen> .
```

- Lanza el contenedor:
```sh
docker run -d --name tranvia --restart=unless-stopped <nombre_de_la_imagen>
```

**NOTA**: No te olvides de poner antes tu token en el fichero de configuración.

## License

Este bot utiliza una licencia GPLv3 - Ver [LICENSE](LICENSE) para más detalles

**[Volver arriba](#tabla-de-contenidos)**