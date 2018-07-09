# Tranvia Zaragoza - Telegram Bot

Bot de telegram que indica a los usuarios los tiempos de llegada de los tranvías
de zaragoza a las distintas paradas

## Tabla de contenidos

- [Tranvia Zaragoza - Telegram Bot](#tranvia-zaragoza---telegram-bot)
    - [Tabla de contenidos](#tabla-de-contenidos)
    - [Comenzando](#comenzando)
        - [Requisitos](#requisitos)
        - [Instalacion](#instalacion)
    - [Running the tests](#running-the-tests)
        - [Break down into end to end tests](#break-down-into-end-to-end-tests)
        - [And coding style tests](#and-coding-style-tests)
    - [Deployment](#deployment)
    - [Built With](#built-with)
    - [Contributing](#contributing)
    - [Versioning](#versioning)
    - [Authors](#authors)
    - [License](#license)
    - [Acknowledgments](#acknowledgments)

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

## Running the tests

Explain how to run the automated tests for this system

**[Volver arriba](#tabla-de-contenidos)**

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

**[Volver arriba](#tabla-de-contenidos)**

### And coding style tests

Explain what these tests test and why

```
Give an example
```

**[Volver arriba](#tabla-de-contenidos)**

## Deployment

Add additional notes about how to deploy this on a live system

**[Volver arriba](#tabla-de-contenidos)**

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

**[Volver arriba](#tabla-de-contenidos)**

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

**[Volver arriba](#tabla-de-contenidos)**

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

**[Volver arriba](#tabla-de-contenidos)**

## Authors

* **....** - *Initial work* - [...](https://github.com)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

**[Volver arriba](#tabla-de-contenidos)**

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

**[Volver arriba](#tabla-de-contenidos)**

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc

**[Volver arriba](#tabla-de-contenidos)**