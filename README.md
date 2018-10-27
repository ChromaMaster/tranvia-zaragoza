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
        - [Usando Docker Compose](#usando-docker-compose)
    - [Monitorización y estadísticas](#monitorización-y-estadísticas)
        - [Base de datos](#base-de-datos)
    - [Control de acceso](#control-de-acceso)
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
[Pipenv][1] la cual ayuda al encapsulamiento del proyecto.

Para poder hacer uso de esto hará falta instalarlo en tu sistema. Una vez instalado
las demás dependencias estan definidas en el fichero [Pipfile](Pipfile). Para
instalarlas, simplemente ejecuta el comando `pipenv install`

- [Python Telegram Bot][2]
- [Requests][3]
- [PyYAML][4]
- [pytz][5]
- [influxdb][9]

**[Volver arriba](#tabla-de-contenidos)**

### Instalacion

Para inicial el bot, lo primero que hace falta es definir una variable de entorno
con el token de nuestro bot obtenido del [BotFather][6].

Para iniciar el bot, y tras haber obtenido un **token** del [BotFather][6] hay 
que entrar dentro del **venv** y crear una variable de entorno que contenga esta
token.

Para ello primero entramos dentro del **venv** utilizando el siguiente comando:

```sh
pipenv shell
```

y creamos la **variable de entorno**:

```sh
export BOT_TOKEN=<TU_TOKEN_AQUI>
```

Con esto ya se puede ejecutar el bot utilizando

```sh
python3 main.py
```

**[Volver arriba](#tabla-de-contenidos)**

### Usando Docker

Para desplegar este bot utilizando Docker puedes seguir los siguientes pasos.

- Constryue la imagen utilizando el [Dockerfile](Dockerfile) proporcionado

```sh
docker build -t <nombre_de_la_imagen> .
```

- Lanza el contenedor:
 
```sh
docker run -d 
    --name tranvia 
    -e "BOT_TOKEN=<TU_TOKEN_AQUI>"
    --restart=unless-stopped <nombre_de_la_imagen>
```

**[Volver arriba](#tabla-de-contenidos)**

### Usando Docker Compose

Utilizando docker-compose puedes desplegar utilizando el siguiente comando:

```sh
docker-compose up -d
```

**[Volver arriba](#tabla-de-contenidos)**

## Monitorización y estadísticas

Existe la posibilidad de obtener métricas acerca de la utilización del bot utilizando
la base de datos **InfluxDB**. **Por defecto la monitorización esta desactivada**.

Las métricas que se pueden obtener son:

- Número de peticiones peticiones que se han hecho
- Número de usuarios totales
- Ranking de utilización de las paradas

Para activar la monitorización se deben definir las siguientes variables de entorno:

- MONITORING_HOST: Dirección de la máquina donde se encuentre la base de datos InfluxDB.
- MONITORING_PORT: Puerto en el que escucha la base de datos.
- MONITORING_USER: El usuario.
- MONITORING_PASS: Contraseña.
- MONITORING_DATABASE_NAME: Nombre de la base de datos.
  
**IMPORTANTE**: En caso de que se quiera utilizar **docker-compose** para la 
puesta en marcha, se deben descomentar las lineas indicadas dentro del fichero 
**docker-compose.yaml**

**[Volver arriba](#tabla-de-contenidos)**

### Base de datos

Para la puesta en marcha de la base de datos se puede utilizar docker:

```sh
docker run -d -p 8086:8086 -v `pwd`/influxdb:/var/lib/influxdb influxdb
```

Para mas opciones de puesta en marcha de un contenedor con InfluxDB mirar
la documentación en el DockerHub: [https://hub.docker.com/_/influxdb/][7]

Para otras puestas en marcha consultar la documentación de InfluxDB:
[https://docs.influxdata.com/influxdb/v1.6/introduction/installation/][8]

**[Volver arriba](#tabla-de-contenidos)**

## Control de acceso

Existen comandos que solo se pueden ejecutar por ciertos usuarios del bot, como
por ejemplo el comando `/stats` que muestra las estadisticas de uso.

Para definir el usuario que puede utilizar este comando se debe definir una
variable de entorno con el ID de Telegram correspondiente.

export BOT_ADMIN_ID=<id_telegram>

**NOTA**: En caso de no conocer tu id de telegram, si no asignas uno e intentas
ejecutar un comando que necesita permiso de admin, se te devolvera un mensaje donde
se indicará tu id. Un ejemplo:

>>> ERROR: BOT_ADMIN_ID no definido. debes definirlo para ejecutar los comandos 
>>> de administrador.
>>>
>>> Si tu eres el administrador, tu id es <TU_ID_ESTA_AQUI>

**[Volver arriba](#tabla-de-contenidos)**

## License

Este bot utiliza una licencia GPLv3 - Ver [LICENSE](LICENSE) para más detalles

**[Volver arriba](#tabla-de-contenidos)**

[1]: https://docs.pipenv.org/
[2]: https://github.com/python-telegram-bot/python-telegram-bot
[3]: http://docs.python-requests.org/en/master/
[4]: http://pyyaml.org/wiki/PyYAMLDocumentation
[5]: http://pytz.sourceforge.net/
[6]: https://telegram.me/BotFather
[7]: https://hub.docker.com/_/influxdb/
[8]: https://docs.influxdata.com/influxdb/v1.6/introduction/installation/
[9]: https://www.influxdata.com/