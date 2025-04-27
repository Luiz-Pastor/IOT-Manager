## 1. Introduccion
El objetivo de este documento es mostrar las funcionalidades de los IOT implementados, así como los formatos que siguen

## 2. Dispositivos IOT
Cada dispositivo IOT tiene 2 topics:
- `redes/2312/10/\<iot-id>` : topic en el cual el dispositivo IOT publica, cuando su implementación lo especifique, su estado. También es donde se mostrará la salida de los comandos que el usuario realize
- `redes/2312/10/\<iot-id>/command` : topic en el cual, el usuario/controlador, manda los comandos, que serán interpretados por el el dispositivo, y cuya salida al comando será mostrada en el pimer topic comentado

Por otra parte, todos los mensajes del sistema han de ir en formato JSON.

### 2.1. Dummy Switch
Cumple el objetivo de un switch. Cuando recibe un mensaje para cambiar su estado, lo intenta realizar (con una probabilidad, por defecto del 30%, de que falle en el proceso).

#### 2.1.1. RFC de mensajes
El dispositivo no varía su valor de forma autónoma sin ayuda, ya que es el usuario el que tiene que asignar un estado. Por ello, se han implementado dos estados:
* `set`: con él, puedes establecer el estado del switch. Junto al comando, también hay que especificar el estado, en el campo "state", al cuál se quiere cambiar
	```json
	{
		"cmd": "set",
		"state": "ON" // or OFF
	}
	/* Posible respuesta: {"state": "ON"} */
	```
* `get`: sirve para obtener el estado actual del dispositivo.
	```json
	{
		"cmd": "get"
	}
	/* Posible respuesta: {"state": "OFF"} */
	```

### 2.2. Dummy Sensor
Simula un sensor que, cada cierto tiempo, cambia su valor. Está implementado de forma que, cuando llegue al valor máximo o mínimo, cambie la dirección en la que va variando el valor del dispositivo: es decir, el incremento se invierte

#### 2.2.1. RFC de mensajes
El dispositivo va variando solo, de forma autónoma, por lo que el único comando necesario es aquel para saber el estado/valor actual del dispositivo:
* `get`: como se menciona, es una orden para que el dispositivo envíe, por su canal predeterminado, el valor actual del sensor.
	```json
	{
		"cmd": "get"
	}
	/* Posible respuesta:  {"state": 25.0} */
	```

### 2.3. Dummy Clock
Simulador de relok. Se le puede especificar cada cuanto el tiempo ha de ser registrado en el topic general

#### 2.3.1. RFC de mensajes
Al igual que en el sensor, funciona automáticamente, lo único necesario sería saber el estado actual del reloj, es decir, sacar la hora de el mismo momento.
* `get`: publica un mensaje con la hora actual
	```json
	{
		"cmd": "get"
	}
	/* Posible respuesta:  {"state": "12:00:04"} */
	```