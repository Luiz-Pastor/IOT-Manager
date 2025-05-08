# Práctica 3

## Instalación
Para que todo el sistema funcione correctamente, es necesario instalar el entorno virtual con el `requirements.txt` proporcionado:
```bash
# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
python3 -m pip install -r requirements.txt
```

Una vez hecho, es necesario realizar las migraciones de Django, de forma que la base de datos tenga la estructura correcta. Por ello, estando en la carpeta `iot-manage`:
```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

Con esto, todos los requisitos están cumplidos. Los distintos elementos del sistema se pueden ejecutar de las siguientes maneras, estando en la raíz (siguiendo las guías del enunciado, que no se especifican aquí, solo es una guía con las reglas por defecto):
- Controlador:
	```bash
	python3 -m controller.controller
	```

- Dispositivos IoT:
	```bash
	python3 -m iot.dummy-switch <id>
	python3 -m iot.dummy-sensor <id>
	python3 -m iot.dummy-clock <id>
	```

- Proyecto de Django (estando en `iot-manage`):
	```bash
	python3 manage.py runserver # Se puede especificar puerto si hace falta
	```

> **NOTA IMPORTANTE:**  
> Por defecto, se toma el valor del host como el supuesto servidor de Mosquitto de la EPS; no obstante, este no es funcional. Es necesario proporcionar `--host localhost` o la ruta por defecto donde el servidor de Mosquitto esté ejecutándose.

Además de los parámetros por defecto, tanto los IoT como el controlador manejan el parámetro `--debug` (por defecto en `false`), que sirve para mostrar mensajes relevantes.

En el Makefile proporcionado, hay atajos (`controller`, `manager`) para lanzar el controlador y el proyecto de Django, respectivamente. Además, también se encuentran otras dos utilidades:
- `mosquitto`: crea un contenedor de Eclipse Mosquitto totalmente funcional en localhost con su puerto por defecto.
- `mosquitto-web-ui`: crea un contenedor de `emqx/mqttx-web`, el cual ofrece una interfaz gráfica sencilla para ver mensajes de los topics de un sistema en concreto, perfecto al principio para observar el comportamiento de los dispositivos IoT.

## Requisitos
- Crear, eliminar, editar y observar la información de los dispositivos.
- Crear, eliminar, editar y observar la información de las reglas.
- Crear una interfaz para que el usuario pueda interactuar con los elementos del sistema.
- Implementar 3 tipos de dispositivos (DummySwitch, DummySensor, DummyClock).
- Implementar el controlador del sistema (y el Rule Engine por separado si fuera necesario).

## Decisiones
- **¿Controller y Rule Engine han de ser aplicaciones separadas?, ¿por qué?, ¿qué ventajas tiene una y otra opción?**  
	En caso de hacerlo separado, el controlador solo debería escuchar los dispositivos, enviar la información al Rule Engine, escuchar del Rule Engine y enviar datos a los topics "commands" de los dispositivos. No obstante, creemos que el Rule Engine se podría ejecutar en el propio controlador. De esta forma, nos quitamos el paso de mantener una nueva conexión. Además, los accesos a la base de datos están optimizados, así que el tiempo perdido en nuestra implementación es menor que el que se perdería con dos entidades independientes.

- **¿Cómo se comunican Controller y Rule Engine en la opción escogida?**  
	Al estar ambas en el controlador, el Rule Engine sería el hilo que se crea al recibir un mensaje del topic de algún dispositivo.

- **¿Tiene sentido que alguno de estos componentes compartan funcionalidad?, ¿qué relación hay entre ellos?**  
	A nuestro parecer, tenerlos separados sería más difícil de manejar. El controlador en verdad debería ser el encargado de manejar todo el sistema. Hacerlo depender de una unidad externa podría generar problemas.

- **¿Cuántas instancias hay de cada componente?**  
	Todos los componentes pueden ser ejecutados en varias instancias. El único requisito con los IoT es que tengan IDs distintos (en caso de lanzarse por cuenta del usuario, en el proyecto de Django esto está limitado).

## Implementaciones
- Los dispositivos están especificados en el documento `doc/iots`.
- El controlador se encarga de escuchar los topics en los que los IoT publican sus estados. En el momento en el que llega un mensaje, se comprueba si dicho dispositivo se encuentra como dispositivo origen de alguna regla; en caso positivo, se comprueba si los parámetros del estado concuerdan con las comparativas y valores de los que está conformada la regla. Si esto se cumple, el mensaje, también especificado en la regla, se envía al dispositivo destino.
- **Rule Engine:** Como se explica en el campo "Decisiones", hemos decidido implementarlo junto con el controlador, sabiendo lo que conlleva.
- El proyecto de Django se encarga de presentar una interfaz agradable en la que un usuario puede crear, eliminar y editar dispositivos y reglas, junto con una sección para ver los logs generados.

## Conclusiones
Nos parece que, para el tiempo dedicado y que hemos tenido para la práctica (creemos que más de 2 semanas eran necesarias, sobre todo teniendo solo 1 clase a la semana y teniendo todas las entregas tan pronto), hemos desarrollado un producto sólido y funcional, con una interfaz bastante sencilla e intuitiva. El sistema de logs y de visualización hace que se sepa perfectamente los dispositivos que se están ejecutando, así como una lista de todas las reglas que están siendo analizadas en el sistema.
